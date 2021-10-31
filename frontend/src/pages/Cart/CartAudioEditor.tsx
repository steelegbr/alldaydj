/**
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {
  Delete,
  Pause, PlayArrow, UploadFile, ZoomIn, ZoomOut,
} from '@mui/icons-material';
import {
  Button, Grid, LinearProgress, Slider,
} from '@mui/material';
import { Cart, CartAudio } from 'api/models/Cart';
import { getCartAudio } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import { CartEditorContext } from 'components/context/CartEditorContext';
import CuePointEditor, { CuePoint } from 'pages/Cart/CuePointEditor';
import React, { ChangeEvent } from 'react';
import { getLogger } from 'services/LoggingService';
import WaveSurfer from 'wavesurfer.js';
import MarkersPlugin from 'wavesurfer.js/src/plugin/markers';

enum CueSetAction {
  LessThan,
  GreaterThan,
  Equal
}

type AudioEditorState = 'Idle' | 'InfoLoading' | 'AudioLoading' | 'Loaded' | 'Error' | 'NoAudio' | 'StartLocalLoading' | 'LocalLoading';
const CUE_POINT_ORDER = [CuePoint.Start, CuePoint.IntroEnd, CuePoint.Segue, CuePoint.End];

const CartAudioEditor = (): React.ReactElement => {
  const [editorState, setEditorState] = React.useState<AudioEditorState>('Idle');
  const [audioLoadProgress, setAudioLoadProgress] = React.useState<number>(0);
  const [zoomLevel, setZoomLevel] = React.useState<number>(1);
  const [audioPlaying, setAudioPlaying] = React.useState<boolean>(false);
  const [localFile, setLocalFile] = React.useState<File>();
  const { cart, setCart } = React.useContext(CartEditorContext);
  const cartId = cart?.id;

  const waveform = React.useRef<HTMLDivElement>(null);
  const wavesurfer = React.useRef<WaveSurfer | null>(null);

  React.useEffect(
    () => {
      getLogger().info('Call to update markers.');
      if (cart && wavesurfer.current) {
        wavesurfer.current.clearMarkers();
        wavesurfer.current.addMarker({
          time: cart.cue_audio_start / 1000,
          color: '#000000',
          position: 'top',
        });
        wavesurfer.current.addMarker({
          time: cart.cue_intro_end / 1000,
          color: '#00FF00',
        });
        wavesurfer.current.addMarker({
          time: cart.cue_segue / 1000,
          color: '#FFFF00',
        });
        wavesurfer.current.addMarker({
          time: cart.cue_audio_end / 1000,
          color: '#000000',
          position: 'top',
        });
        getLogger().info('Updated markers.');
      } else {
        getLogger().warn('Failed to update markers.');
      }
    },
    [cart],
  );

  const seekCallback = React.useCallback(
    (position: number) => {
      if (wavesurfer.current) {
        const audioLength = wavesurfer.current.getDuration() * 1000;
        const seekFraction = position / audioLength;
        wavesurfer.current.seekTo(seekFraction);
        getLogger().info(`Seeking to {audioLength} ms (${seekFraction} of the clip)`);
      }
    },
    [wavesurfer],
  );

  const calculateCueValue = React.useCallback(
    (currentPosition: number, newPosition: number, action: CueSetAction) => {
      switch (action) {
        case CueSetAction.LessThan:
          return (currentPosition >= newPosition) ? newPosition : currentPosition;
        case CueSetAction.GreaterThan:
          return (currentPosition <= newPosition) ? newPosition : currentPosition;
        default:
          return newPosition;
      }
    },
    [],
  );

  const setCuePoint = React.useCallback(
    (selectedCuePoint: CuePoint, position: number, action: CueSetAction): Partial<Cart> => {
      if (cart) {
        switch (selectedCuePoint) {
          case CuePoint.Start:
            return { cue_audio_start: calculateCueValue(cart.cue_audio_start, position, action) };
          case CuePoint.IntroEnd:
            return { cue_intro_end: calculateCueValue(cart.cue_intro_end, position, action) };
          case CuePoint.Segue:
            return { cue_segue: calculateCueValue(cart.cue_segue, position, action) };
          default:
            return { cue_audio_end: calculateCueValue(cart.cue_audio_end, position, action) };
        }
      }
      return {};
    },
    [cart, calculateCueValue],
  );

  const setCuePointCallback = React.useCallback(
    (selectedCuePoint: CuePoint) => {
      if (wavesurfer.current && cart) {
        const currentPosition = wavesurfer.current.getCurrentTime() * 1000;
        getLogger().info(`Settings marker ${selectedCuePoint} to ${currentPosition} ms.`);

        let foundCurrent = false;
        let cuePoints: Partial<Cart> = {};

        for (let i = 0; i < CUE_POINT_ORDER.length; i += 1) {
          if (CUE_POINT_ORDER[i] === selectedCuePoint) {
            foundCurrent = true;
            cuePoints = {
              ...cuePoints,
              ...setCuePoint(CUE_POINT_ORDER[i], currentPosition, CueSetAction.Equal),
            };
          } else if (foundCurrent) {
            cuePoints = {
              ...cuePoints,
              ...setCuePoint(CUE_POINT_ORDER[i], currentPosition, CueSetAction.GreaterThan),
            };
          } else {
            cuePoints = {
              ...cuePoints,
              ...setCuePoint(CUE_POINT_ORDER[i], currentPosition, CueSetAction.LessThan),
            };
          }
        }

        const updatedCart = {
          ...cart,
          ...cuePoints,
        };

        setCart(updatedCart);
      }
    },
    [wavesurfer, cart, setCart, setCuePoint],
  );

  const generateWavesurfer = React.useCallback(
    () => {
      if (waveform.current) {
        const newWavesurfer = WaveSurfer.create(
          {
            container: waveform.current,
            splitChannels: true,
            plugins: [
              MarkersPlugin.create({}),
            ],
          },
        );

        newWavesurfer.on('ready', () => {
          setEditorState('Loaded');
          newWavesurfer.zoom(zoomLevel);
        });

        newWavesurfer.on('waveform-ready', () => {
          setEditorState('Loaded');
          newWavesurfer.zoom(zoomLevel);
        });

        newWavesurfer.on('loading', (progress: number) => {
          setAudioLoadProgress(progress);
        });

        newWavesurfer.on('finish', () => {
          setAudioPlaying(false);
        });

        newWavesurfer.on('pause', () => {
          setAudioPlaying(false);
        });

        newWavesurfer.on('play', () => {
          setAudioPlaying(true);
        });

        newWavesurfer.on('error', () => {
          setEditorState('Error');
        });

        return newWavesurfer;
      }
      return null;
    },
    [zoomLevel],
  );

  const loadRemoteAudio = React.useCallback(
    (url: string) => {
      const newWavesurfer = generateWavesurfer();
      if (newWavesurfer) {
        setLocalFile(undefined);
        newWavesurfer.load(url);
        wavesurfer.current = newWavesurfer;
      } else {
        setEditorState('Error');
        getLogger().error('Waveform does not have a live reference.');
      }
    },
    [generateWavesurfer],
  );

  const handleZoomLevelEvent = (event: any, level: number | number [], thumb: number) => {
    getLogger().debug(`Zoom thumb ${thumb}`);

    if (Array.isArray(level)) {
      getLogger().warn('Got multiple zoom level values!');
    } else {
      getLogger().info(`Set zoom level to ${level}`);
      setZoomLevel(level);
      if (wavesurfer.current) {
        wavesurfer.current.zoom(level);
      }
    }
  };

  const handlePlayPause = React.useCallback(
    () => {
      if (wavesurfer.current) {
        if (audioPlaying) {
          getLogger().info('Pausing audio.');
          wavesurfer.current.pause();
        } else {
          getLogger().info('Playing audio.');
          wavesurfer.current.play();
        }
      } else {
        getLogger().warn('Cannot play/pause without a wavesurfer instance.');
      }
    },
    [audioPlaying],
  );

  const clearAudio = () => {
    if (audioPlaying) {
      wavesurfer.current?.pause();
      wavesurfer.current?.destroy();
    }
    setEditorState('NoAudio');
  };

  const loadLocalAudio = React.useCallback(
    () => {
      const newWavesurfer = generateWavesurfer();
      if (newWavesurfer && localFile) {
        newWavesurfer.loadBlob(localFile);
        wavesurfer.current = newWavesurfer;
        setEditorState('LocalLoading');
        getLogger().info(`Loaded the local file ${localFile.name}.`);
      } else {
        setEditorState('Error');
        getLogger().error('Waveform does not have a live reference, we do not have a local file or are in the wrong state.');
      }
    },
    [generateWavesurfer, localFile],
  );

  const handleFileSelection = (event: ChangeEvent<HTMLInputElement>) => {
    const { files } = event.target;
    if (files) {
      const file = files[0];
      getLogger().log(`Changing file from ${localFile?.name} to ${file.name}`);
      setLocalFile(file);
      setEditorState('StartLocalLoading');
    }
  };

  React.useEffect(
    () => {
      if (cartId && editorState === 'Idle') {
        getLogger().info(`Downloading cart audio info for cart ${cartId}`);
        setEditorState('InfoLoading');
        getCartAudio(cartId).then(
          (response: AxiosResponse<CartAudio>) => {
            if (response.status === 200) {
              getLogger().info('Found audio information.');
              setEditorState('AudioLoading');
              loadRemoteAudio(response.data.audio);
            } else {
              getLogger().warn('Found no audio information.');
              setEditorState('NoAudio');
            }
          },
          (error) => {
            getLogger().warn(`Encountered error ${error} obtaining audio information.`);
            setEditorState('NoAudio');
          },
        );
      } else if (editorState === 'StartLocalLoading') {
        loadLocalAudio();
      }
    },
    [cartId, editorState, loadLocalAudio, loadRemoteAudio],
  );

  const audioControls = () => (
    <Grid alignItems="center" container direction="column" justifyContent="space-between">
      <Grid container direction="row" justifyContent="space-between">
        <Grid item>
          <Button onClick={handlePlayPause} variant="contained">
            {audioPlaying ? <Pause /> : <PlayArrow />}
            {audioPlaying ? 'Pause' : 'Play'}
          </Button>
        </Grid>
        <Grid item>
          <Button onClick={clearAudio} variant="contained">
            <Delete />
            Clear Audio
          </Button>
        </Grid>
      </Grid>
      <Grid container direction="row" justifyContent="center">
        <Grid item xs={1}>
          <ZoomOut />
        </Grid>
        <Grid item xs={10}>
          <Slider aria-label="audio editor zoom" max={200} min={1} onChange={handleZoomLevelEvent} value={zoomLevel} />
        </Grid>
        <Grid item xs={1}>
          <ZoomIn />
        </Grid>
      </Grid>
      <Grid container direction="row" justifyContent="space-between">
        <CuePointEditor
          cuePoint={CuePoint.Start}
          seekCallback={seekCallback}
          setCallback={setCuePointCallback}
        />
        <CuePointEditor
          cuePoint={CuePoint.IntroEnd}
          seekCallback={seekCallback}
          setCallback={setCuePointCallback}
        />
        <CuePointEditor
          cuePoint={CuePoint.Segue}
          seekCallback={seekCallback}
          setCallback={setCuePointCallback}
        />
        <CuePointEditor
          cuePoint={CuePoint.End}
          seekCallback={seekCallback}
          setCallback={setCuePointCallback}
        />
      </Grid>
    </Grid>
  );

  const loadingProgress = () => (
    <LinearProgress value={audioLoadProgress} variant="determinate" />
  );

  if (editorState === 'Idle' || editorState === 'NoAudio') {
    return (
      <Button component="label" variant="contained">
        <UploadFile />
        Upload File
        <input accept=".wav,.mp3,.ogg" hidden onChange={handleFileSelection} type="file" />
      </Button>
    );
  }

  if (editorState === 'InfoLoading') {
    return (
      <LinearProgress variant="indeterminate" />
    );
  }

  return (
    <>
      <div id="waveform" ref={waveform} />
      {(editorState === 'AudioLoading' || editorState === 'LocalLoading') && loadingProgress()}
      {editorState === 'Loaded' && audioControls()}
    </>
  );
};

export default CartAudioEditor;
