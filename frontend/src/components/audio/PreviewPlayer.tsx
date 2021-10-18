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

import React from 'react';
import { PreviewContext } from 'components/context/PreviewContext';
import {
  Alert,
  Button,
  ButtonGroup,
  CircularProgress,
  Drawer,
  Grid,
  Slider,
  Typography,
} from '@mui/material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
import { getLogger } from 'services/LoggingService';
import {
  Close, Pause, PlayArrow, Stop,
} from '@mui/icons-material';
import { getCartAudio, getCartDetails } from 'api/requests/Cart';
import { Cart, CartAudio } from 'api/models/Cart';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import { AxiosResponse } from 'axios';
import { millisecondToMinutesSecond } from 'services/TimeService';
import { useInterval } from 'usehooks-ts';

type PreviewPlayerState = 'Idle' | 'Loading' | 'Playing' | 'Paused' | 'Error';

const useStyles = makeStyles(() => createStyles({
  player: {
    padding: 10,
  },
  spinner: {
    padding: 10,
    size: 10,
  },
}));

const PreviewPlayer = () : React.ReactElement => {
  const classes = useStyles();
  const previewContext = React.useContext(PreviewContext);
  const authenticationContext = React.useContext(AuthenticationContext);
  const [loadedCartId, setLoadedCartId] = React.useState<string>();
  const [playerState, setPlayerState] = React.useState<PreviewPlayerState>('Idle');
  const [cart, setCart] = React.useState<Cart>();
  const [cartAudio, setCartAudio] = React.useState<CartAudio>();
  const [progress, setProgress] = React.useState<number>(0);
  const [scrubbing, setScrubbing] = React.useState<boolean>(false);
  const audioRef = React.useRef(new Audio());

  const { cartId, clearCart } = previewContext;
  const token = authenticationContext?.authenticationStatus.accessToken;
  const showDrawer = !!(cartId);
  const enablePlayPauseButton = playerState === 'Playing' || playerState === 'Paused';

  const scrubTo = (position: number) => {
    audioRef.current.currentTime = position / 1000;
    getLogger().debug(`Scrubbing to ${position} ms.`);
    setProgress(position);
  };

  const playAudio = () => {
    getLogger().info('Audio play triggered.');
    audioRef.current.play();
    setPlayerState('Playing');
  };

  // skipcq: JS-0323
  const scrubAction = (event: any, position: number | number [], thumb: number) => {
    getLogger().debug(`Scrubbing thumb number: ${thumb}`);
    setScrubbing(true);
    if (Array.isArray(position)) {
      scrubTo(position[0]);
    } else {
      scrubTo(position);
    }
  };

  const scrubEnd = () => {
    getLogger().debug('Scrub stopped.');
    setScrubbing(false);
  };

  const stopAudio = React.useCallback(
    (returnToStart: boolean) => {
      getLogger().info('Audio stop triggered.');
      audioRef.current.pause();
      setPlayerState('Paused');
      if (returnToStart && cart) {
        getLogger().info('Resetting to start of audio.');
        scrubTo(cart.cue_audio_start);
      }
    },
    [cart],
  );

  const playPauseClick = React.useCallback(
    () => {
      if (playerState === 'Playing') {
        getLogger().info('Pause click.');
        stopAudio(false);
      } else {
        getLogger().info('Play click.');
        playAudio();
      }
    },
    [playerState, stopAudio],
  );

  const clearPlayingCart = React.useCallback(
    () => {
      getLogger().info('Unloading audio from player.');
      stopAudio(true);
      audioRef.current.src = '';
      setPlayerState('Idle');
      setCartAudio(undefined);
    },
    [stopAudio],
  );

  const stopClick = () => {
    getLogger().info('Stop click.');
    stopAudio(true);
  };

  const closeClick = () => {
    getLogger().info('Close click.');
    clearPlayingCart();
    clearCart();
  };

  const loadCartAudioInfo = React.useCallback(
    (requestedCartId: string, requestToken: string) => {
      getLogger().info(`Loading cart audio information for ${requestedCartId} to preview.`);
      getCartAudio(requestedCartId, requestToken).then(
        (response: AxiosResponse<CartAudio>) => {
          if (response.status === 200) {
            setCartAudio(response.data);
          } else {
            getLogger().error(`Error encountered unexpected status of ${response.status} loading the cart audio info for preview.`);
            setPlayerState('Error');
          }
        },
        (error) => {
          getLogger().error(`Error encountered loading the cart audio info for preview: ${error}`);
          setPlayerState('Error');
        },
      );
    },
    [],
  );

  React.useEffect(
    () => {
      if (cart && cartAudio) {
        getLogger().info(`Setting audio component SRC to ${cartAudio.compressed}`);
        audioRef.current = new Audio(cartAudio.compressed);
        scrubTo(cart.cue_audio_start);
        playAudio();
      }
    },
    [cart, cartAudio],
  );

  React.useEffect(
    () => {
      if (cartId && cartId !== loadedCartId && token) {
        clearPlayingCart();
        setPlayerState('Loading');
        setLoadedCartId(cartId);
        getLogger().info(`Loading cart ${cartId} for preview.`);
        getCartDetails(cartId, token).then(
          (response: AxiosResponse<Cart>) => {
            if (response.status === 200) {
              setCart(response.data);
              setLoadedCartId(cartId);
              loadCartAudioInfo(cartId, token);
            } else {
              getLogger().error(`Encountered unexpected status code of ${response.status} loading the cart for preview.`);
              setPlayerState('Error');
            }
          },
          (error) => {
            getLogger().error(`Error encountered loading the cart for preview: ${error}`);
            setPlayerState('Error');
          },
        );
      }
    },
    [
      cartId,
      setPlayerState,
      token,
      loadedCartId,
      setLoadedCartId,
      loadCartAudioInfo,
      clearPlayingCart,
    ],
  );

  useInterval(
    () => {
      const currentPosition = audioRef.current.currentTime * 1000;
      setProgress(currentPosition);

      if (audioRef.current.error) {
        setPlayerState('Error');
      }

      if (cart && (audioRef.current.ended || currentPosition >= cart.cue_audio_end)) {
        stopAudio(true);
      }
    },
    (playerState === 'Playing' || playerState === 'Paused') && !scrubbing ? 500 : null,
  );

  const buttonBar = () => (
    <Grid alignItems="center" container justifyContent="space-between">
      <Grid item>
        <ButtonGroup aria-label="preview cart" variant="contained">
          <Button
            disabled={!enablePlayPauseButton}
            onClick={playPauseClick}
            startIcon={playerState === 'Playing' ? <Pause /> : <PlayArrow />}
          >
            {playerState === 'Playing' ? 'Pause' : 'Play'}
          </Button>
          <Button disabled={playerState === 'Error'} onClick={stopClick} startIcon={<Stop />}>Stop</Button>
        </ButtonGroup>
      </Grid>
      <Grid item />
      <Grid item>
        <Button data-test="button-close" onClick={closeClick} startIcon={<Close />}>Close</Button>
      </Grid>
    </Grid>
  );

  const loadingPlaceholder = () => (
    <Grid alignItems="center" container justifyContent="center">
      <Grid item>
        <CircularProgress className={classes.spinner} />
      </Grid>
      <Grid item>
        Loading...
      </Grid>
    </Grid>
  );

  const playerDetails = () => {
    if (cart) {
      const audioLength = cart.cue_audio_end - cart.cue_audio_start;
      const currentPosition = progress - cart.cue_audio_start;
      return (
        <>
          <Typography variant="subtitle1">
            {cart?.display_artist}
          </Typography>
          <Typography variant="subtitle2">
            {cart?.title}
          </Typography>
          <Grid alignItems="center" container justifyContent="space-between" spacing={2}>
            <Grid item xs={1}>
              {millisecondToMinutesSecond(currentPosition)}
            </Grid>
            <Grid item xs={10}>
              <Slider
                aria-label="audio preview time indicator"
                max={audioLength}
                min={0}
                onChange={scrubAction}
                onKeyUp={scrubEnd}
                onMouseUp={scrubEnd}
                step={1}
                value={currentPosition}
              />
            </Grid>
            <Grid alignContent="flex-end" item xs={1}>
              {millisecondToMinutesSecond(audioLength)}
            </Grid>
          </Grid>
        </>
      );
    }

    return <></>;
  };

  const errorMessage = () => <Alert data-test="preview-error" severity="error" variant="outlined">Something went wrong trying to preview cart audio. Please try again later.</Alert>;

  if (showDrawer) {
    return (
      <Drawer anchor="bottom" open={showDrawer} variant="permanent">
        <div className={classes.player}>
          {buttonBar()}
          {playerState === 'Loading' && loadingPlaceholder()}
          {playerState === 'Error' && errorMessage()}
          {(playerState === 'Playing' || playerState === 'Paused') && playerDetails()}
        </div>
      </Drawer>
    );
  }

  return <></>;
};

export default PreviewPlayer;
