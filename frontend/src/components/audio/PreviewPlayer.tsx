import React from 'react';
import { PreviewContext } from 'components/context/PreviewContext';
import {
  Button,
  ButtonGroup,
  CircularProgress,
  createStyles,
  Grid,
  makeStyles,
  Slider,
  SwipeableDrawer,
  Typography,
} from '@material-ui/core';
import { getLogger } from 'services/LoggingService';
import {
  Close, Pause, PlayArrow, Stop,
} from '@material-ui/icons';
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
  const log = getLogger();
  const classes = useStyles();
  const previewContext = React.useContext(PreviewContext);
  const authenticationContext = React.useContext(AuthenticationContext);
  const [loadedCartId, setLoadedCartId] = React.useState<string>();
  const [playerState, setPlayerState] = React.useState<PreviewPlayerState>('Idle');
  const [cart, setCart] = React.useState<Cart>();
  const [cartAudio, setCartAudio] = React.useState<CartAudio>();
  const [progress, setProgress] = React.useState<number>(0);
  const audioRef = React.useRef(new Audio());

  const { cartId } = previewContext;
  const token = authenticationContext?.authenticationStatus.accessToken;
  const showDrawer = !!(cartId);
  const enablePlayPauseButton = playerState === 'Playing' || playerState === 'Paused';
  const noOp = () => {};

  const loadCartAudioInfo = React.useCallback(
    (requestedCartId: string, requestToken: string) => {
      log.info(`Loading cart audio information for ${requestedCartId} to preview.`);
      getCartAudio(requestedCartId, requestToken).then(
        (response: AxiosResponse<CartAudio>) => {
          setCartAudio(response.data);
        },
        (error) => {
          log.error(`Error encountered loading the cart audio info for preview: ${error}`);
          setPlayerState('Error');
        },
      );
    },
    [log],
  );

  React.useEffect(
    () => {
      if (cart && cartAudio) {
        audioRef.current = new Audio(cartAudio.compressed);
        audioRef.current.currentTime = cart.cue_audio_start / 1000;
        audioRef.current.play();
        setPlayerState('Playing');
      }
    },
    [cart, cartAudio],
  );

  React.useEffect(
    () => {
      if (cartId && cartId !== loadedCartId && token) {
        setPlayerState('Loading');
        setLoadedCartId(cartId);
        log.info(`Loading cart ${cartId} for preview.`);
        getCartDetails(cartId, token).then(
          (response: AxiosResponse<Cart>) => {
            setCart(response.data);
            setLoadedCartId(cartId);
            loadCartAudioInfo(cartId, token);
          },
          (error) => {
            log.error(`Error encountered loading the cart for preview: ${error}`);
            setPlayerState('Error');
          },
        );
      }
    },
    [cartId, setPlayerState, log, token, loadedCartId, setLoadedCartId, loadCartAudioInfo],
  );

  useInterval(
    () => {
      setProgress(audioRef.current.currentTime * 1000);
      if (audioRef.current.error) {
        setPlayerState('Error');
      }
    },
    playerState === 'Playing' || playerState === 'Paused' ? 500 : null,
  );

  const buttonBar = () => (
    <Grid alignItems="center" container justifyContent="space-between">
      <Grid item>
        <ButtonGroup aria-label="preview cart" variant="contained">
          <Button
            disabled={!enablePlayPauseButton}
            startIcon={playerState === 'Playing' ? <Pause /> : <PlayArrow />}
          >
            {playerState === 'Playing' ? 'Pause' : 'Play'}
          </Button>
          <Button startIcon={<Stop />}>Stop</Button>
        </ButtonGroup>
      </Grid>
      <Grid item />
      <Grid item>
        <Button startIcon={<Close />}>Close</Button>
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

  const errorMessage = () => {
    <Grid alignItems="center" container justifyContent="center">
      <Grid item>
        <span>Something went wrong trying to preview cart audio. Please try again later.</span>
      </Grid>
    </Grid>;
  };

  if (showDrawer) {
    return (
      <SwipeableDrawer anchor="bottom" onClose={noOp} onOpen={noOp} open={showDrawer} variant="permanent">
        <div className={classes.player}>
          {buttonBar()}
          {playerState === 'Loading' && loadingPlaceholder()}
          {playerState === 'Error' && errorMessage()}
          {(playerState === 'Playing' || playerState === 'Paused') && playerDetails()}
        </div>
      </SwipeableDrawer>
    );
  }

  return <></>;
};

export default PreviewPlayer;
