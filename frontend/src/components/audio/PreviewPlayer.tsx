import React from 'react';
import { PreviewContext } from 'components/context/PreviewContext';
import {
  Button, ButtonGroup, Grid, SwipeableDrawer,
} from '@material-ui/core';
import { getLogger } from 'services/LoggingService';
import {
  Close, Pause, PlayArrow, Stop,
} from '@material-ui/icons';
import { getCartAudio, getCartDetails } from 'api/requests/Cart';
import { Cart, CartAudio } from 'api/models/Cart';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import { AxiosResponse } from 'axios';

type PreviewPlayerState = 'Idle' | 'Loading' | 'Playing' | 'Paused' | 'Error';

const PreviewPlayer = () : React.ReactElement => {
  const log = getLogger();
  const previewContext = React.useContext(PreviewContext);
  const authenticationContext = React.useContext(AuthenticationContext);
  const [playerState, setPlayerState] = React.useState<PreviewPlayerState>('Idle');
  const [cart, setCart] = React.useState<Cart>();
  const [cartAudio, setCartAudio] = React.useState<CartAudio>();

  const { cartId } = previewContext;
  const token = authenticationContext?.authenticationStatus.accessToken;
  const showDrawer = cartId !== undefined;
  const enablePlayPauseButton = playerState === 'Playing' || playerState === 'Paused';
  const noOp = () => {};

  React.useEffect(
    () => {
      if (cartId && token) {
        setPlayerState('Loading');
        log.info(`Loading cart ${cartId} for preview.`);
        getCartDetails(cartId, token).then(
          (response: AxiosResponse<Cart>) => {
            setCart(response.data);
          },
          (error) => {
            log.error(`Error encountered loading the cart for preview: ${error}`);
            setPlayerState('Error');
          },
        );
      }
    },
    [cartId, setPlayerState, log, token],
  );

  React.useEffect(
    () => {
      if (cartId && token) {
        log.info(`Loading cart audio information for ${cartId} to preview.`);
        getCartAudio(cartId, token).then(
          (response: AxiosResponse<CartAudio>) => {
            setCartAudio(response.data);
            setPlayerState('Paused');
          },
          (error) => {
            log.error(`Error encountered loading the cart audio info for preview: ${error}`);
            setPlayerState('Error');
          },
        );
      }
    },
    [cart, cartId, token, log],
  );

  console.log(cartAudio);

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

  const loadingPlaceholder = () => {
    <p>Loading...</p>;
  };

  return (
    <SwipeableDrawer anchor="bottom" onClose={noOp} onOpen={noOp} open={showDrawer} variant="permanent">
      {buttonBar()}
      {playerState === 'Loading' && loadingPlaceholder()}
    </SwipeableDrawer>
  );
};

export default PreviewPlayer;
