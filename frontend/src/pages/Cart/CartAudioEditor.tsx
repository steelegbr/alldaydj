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
  Pause, PlayArrow, ZoomIn, ZoomOut,
} from '@mui/icons-material';
import {
  Button, Grid, LinearProgress, Slider,
} from '@mui/material';
import { Cart, CartAudio } from 'api/models/Cart';
import { getCartAudio } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import React from 'react';
import { FileUploader } from 'react-drag-drop-files';
import { getLogger } from 'services/LoggingService';
import WaveSurfer from 'wavesurfer.js';
import MarkersPlugin from 'wavesurfer.js/src/plugin/markers';

// const SUPPORTED_FILE_TYPES = ['wav', 'mp3', 'ogg'];

type AudioEditorState = 'Idle' | 'InfoLoading' | 'AudioLoading' | 'Loaded' | 'Error' | 'NoAudio' | 'StartLocalLoading' | 'LocalLoading';

interface CartAudioEditorProps {
  cart: Cart
}

const CartAudioEditor = (
  { cart }: CartAudioEditorProps,
): React.ReactElement => {
  const [editorState, setEditorState] = React.useState<AudioEditorState>('Idle');
  const [audioLoadProgress, setAudioLoadProgress] = React.useState<number>(0);
  const [zoomLevel, setZoomLevel] = React.useState<number>(1);
  const [audioPlaying, setAudioPlaying] = React.useState<boolean>(false);
  const [localFile, setLocalFile] = React.useState<File>();
  const authenticatonContext = React.useContext(AuthenticationContext);
  const token = authenticatonContext?.authenticationStatus.accessToken;
  const cartId = cart?.id;

  const waveform = React.useRef<HTMLDivElement>(null);
  const wavesurfer = React.useRef<WaveSurfer | null>(null);

  const loadMarkers = React.useCallback(
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
          time: cart.cue_intro_start / 1000,
          color: '#00FF00',
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
          loadMarkers();
        });

        newWavesurfer.on('waveform-ready', () => {
          setEditorState('Loaded');
          newWavesurfer.zoom(zoomLevel);
          loadMarkers();
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

        return newWavesurfer;
      }
      return null;
    },
    [loadMarkers, zoomLevel],
  );

  const loadRemoteAudio = React.useCallback(
    (url: string) => {
      const newWavesurfer = generateWavesurfer();
      if (newWavesurfer) {
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

  const handleFileSelection = (file: File) => {
    getLogger().log(`Changing file from ${localFile} to ${file.name}`);
    setLocalFile(file);
    setEditorState('StartLocalLoading');
  };

  React.useEffect(
    () => {
      if (cartId && token && editorState === 'Idle') {
        getLogger().info(`Downloading cart audio info for cart ${cartId}`);
        setEditorState('InfoLoading');
        getCartAudio(cartId, token).then(
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
    [cartId, editorState, token, loadLocalAudio, loadRemoteAudio],
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
    </Grid>
  );

  const loadingProgress = () => (
    <LinearProgress value={audioLoadProgress} variant="determinate" />
  );

  if (editorState === 'Idle' || editorState === 'NoAudio') {
    return (
      <FileUploader
        handleChange={handleFileSelection}
        onTypeError={(error) => getLogger().error(error)}
      />
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
