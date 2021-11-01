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
  ArrowBack,
  ArrowForward,
  CheckBox, CheckBoxOutlineBlank, Error,
} from '@mui/icons-material';
import {
  Alert,
  Button,
  CircularProgress, List, ListItem, Typography,
} from '@mui/material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
import { AudioJobStatus, AudioUploadJob, Cart } from 'api/models/Cart';
import {
  createCart, getUploadJobProgress, updateCart, updatePartialCart, uploadAudio,
} from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import React from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import Paths from 'routing/Paths';
import { getLogger } from 'services/LoggingService';
import { useInterval } from 'usehooks-ts';

const ERROR_UPLOAD_AUDIO = 'Something went wrong uploading the audio. Please try again later.';
const ERROR_UPDATE_CART = 'Something went wrong updating the cart. Please try again later.';
const ERROR_UPDATE_CUE_POINTS = 'Something went wrong updating the cue points. Please try again later.';

export interface CartSynchroniserState {
    cart: Cart,
    file?: File
}

enum SyncState {
    Idle,
    UpdatingCart,
    ErrorUpdatingCart,
    UploadingAudio,
    ErrorUploadingAudio,
    ErrorProcessing,
    ErrorSettingCuePoints,
    Queued,
    Validating,
    Decompressing,
    Metadata,
    Compress,
    Hashses,
    SettingCuePoints,
    Complete
}

const useStyles = makeStyles(() => createStyles({
  spinner: {
    padding: 10,
    size: 10,
  },
}));

const MAP_JOB_STATUS_SYNC_STATE = new Map<AudioJobStatus, SyncState>([
  ['QUEUED', SyncState.Queued],
  ['ERROR', SyncState.ErrorProcessing],
  ['VALIDATING', SyncState.Validating],
  ['DECOMPRESSING', SyncState.Decompressing],
  ['METADATA', SyncState.Decompressing],
  ['COMPRESSING', SyncState.Compress],
  ['HASHING', SyncState.Hashses],
  ['DONE', SyncState.SettingCuePoints],
]);

const CartSynchroniser = (): React.ReactElement => {
  const history = useHistory();
  const classes = useStyles();
  const location = useLocation<CartSynchroniserState>();
  const { cart, file } = location.state;
  const [state, setState] = React.useState<SyncState>(SyncState.Idle);
  const [errorText, setErrorText] = React.useState<string>();
  const [updatedCart, setUpdatedCart] = React.useState<Cart>(cart);
  const [uploadProgress, setUploadProgress] = React.useState<number>(0);
  const [audioUploadJob, setAudioUploadJob] = React.useState<AudioUploadJob>();

  const renderProgressIcon = (level: SyncState, errorLevel: SyncState, progress?: number) => {
    if (state < level) {
      return <CheckBoxOutlineBlank />;
    }

    if (state === errorLevel) {
      return <Error color="error" />;
    }

    if (state > level) {
      return <CheckBox color="success" />;
    }

    return progress && progress < 100 ? <CircularProgress className={classes.spinner} value={uploadProgress} variant="determinate" /> : <CircularProgress className={classes.spinner} />;
  };

  const progressCallback = React.useCallback(
    (event: ProgressEvent) => {
      const progress = Math.round((event.loaded / event.total) * 100);
      setUploadProgress(progress);
    },
    [],
  );

  const uploadAudioSuccess = React.useCallback(
    (response: AxiosResponse<AudioUploadJob>) => {
      if (response.status === 200) {
        setState(SyncState.Queued);
        setAudioUploadJob(response.data);
      } else {
        getLogger().error(`Werid response code of ${response.status} uploading the audio.`);
        setErrorText(ERROR_UPLOAD_AUDIO);
        setState(SyncState.ErrorUpdatingCart);
      }
    },
    [],
  );

  const uploadAudioError = React.useCallback(
    (error: Error) => {
      getLogger().error(`Got an error uploading the audio: ${error}`);
      setErrorText(ERROR_UPLOAD_AUDIO);
      setState(SyncState.ErrorUploadingAudio);
    },
    [],
  );

  const updateCartSuccess = React.useCallback(
    (response: AxiosResponse<Cart>) => {
      if (response.status === 200 || response.status === 201) {
        setUpdatedCart(response.data);
        if (file) {
          setState(SyncState.UploadingAudio);
          uploadAudio(
            response.data, file, progressCallback,
          ).then(
            uploadAudioSuccess, uploadAudioError,
          );
        } else {
          setState(SyncState.Complete);
        }
      } else if (response.status === 409) {
        setErrorText(`Another cart with label ${cart.label} already exists.`);
        setState(SyncState.ErrorUpdatingCart);
      } else {
        getLogger().error(`Werid response code of ${response.status} updating the cart.`);
        setErrorText(ERROR_UPDATE_CART);
        setState(SyncState.ErrorUpdatingCart);
      }
    },
    [cart, file, progressCallback, uploadAudioError, uploadAudioSuccess],
  );

  const updateCartError = React.useCallback(
    (error: Error) => {
      getLogger().error(`Got an error updating the cart: ${error}`);
      setErrorText(ERROR_UPDATE_CART);
      setState(SyncState.ErrorUpdatingCart);
    },
    [],
  );

  const returnToPrevious = React.useCallback(
    () => {
      history.goBack();
    },
    [history],
  );

  const goForward = React.useCallback(
    () => {
      history.push(`${Paths.cart}${updatedCart.id}`);
    },
    [history, updatedCart.id],
  );

  const updateCuePointsSuccess = React.useCallback(
    (response: AxiosResponse<Cart>) => {
      if (response.status === 200) {
        setState(SyncState.Complete);
      } else {
        getLogger().warn(`Got response code ${response.status} setting the cue points.`);
        setState(SyncState.ErrorSettingCuePoints);
      }
    },
    [],
  );

  const updateCuePointsError = React.useCallback(
    (error: Error) => {
      getLogger().error(`Got an error setting the cue points: ${error}`);
      setErrorText(ERROR_UPDATE_CUE_POINTS);
      setState(SyncState.ErrorSettingCuePoints);
    },
    [],
  );

  React.useEffect(
    () => {
      setState(SyncState.UpdatingCart);
      if (cart.id) {
        updateCart(cart).then(updateCartSuccess, updateCartError);
      } else {
        createCart(cart).then(updateCartSuccess, updateCartError);
      }
    },
    [cart, updateCartSuccess, updateCartError],
  );

  useInterval(
    () => {
      if (audioUploadJob) {
        getLogger().info('Refreshing job state.');
        getUploadJobProgress(audioUploadJob.id).then(
          (response: AxiosResponse<AudioUploadJob>) => {
            if (response.status === 200) {
              const newState = MAP_JOB_STATUS_SYNC_STATE.get(
                response.data.status,
              ) || SyncState.ErrorProcessing;
              setState(newState);
              if (newState === SyncState.SettingCuePoints) {
                const cuePoints: Partial<Cart> = {
                  id: updatedCart.id,
                  cue_audio_start: updatedCart.cue_audio_start,
                  cue_intro_end: updatedCart.cue_intro_end,
                  cue_segue: updatedCart.cue_segue,
                  cue_audio_end: updatedCart.cue_audio_end,
                };
                updatePartialCart(cuePoints).then(updateCuePointsSuccess, updateCuePointsError);
              }
            } else {
              getLogger().error(`Got status code ${response.status} getting the job status.`);
            }
          },
          (error: Error) => {
            getLogger().error(`Ran into an error getting the job status: ${error}`);
          },
        );
      }
    },
    state >= SyncState.Queued && state < SyncState.SettingCuePoints ? 1000 : null,
  );

  return (
    <>
      <Typography variant="h1">
        {cart.id ? 'Updating Cart' : 'Uploading New Cart'}
      </Typography>
      {errorText && (
        <Alert severity="error">{errorText}</Alert>
      )}
      <List>
        <ListItem>
          {renderProgressIcon(SyncState.UpdatingCart, SyncState.ErrorUpdatingCart)}
          {cart.id ? 'Update Cart' : 'Upload New Cart'}
        </ListItem>
        {file && (
        <>
          <ListItem>
            {renderProgressIcon(
              SyncState.UploadingAudio,
              SyncState.ErrorUploadingAudio,
              uploadProgress,
            )}
            Upload audio
          </ListItem>
          <ListItem>
            {renderProgressIcon(SyncState.Validating, SyncState.ErrorProcessing)}
            Validate audio file
          </ListItem>
          <ListItem>
            {renderProgressIcon(SyncState.Decompressing, SyncState.ErrorProcessing)}
            Decompress audio file
          </ListItem>
          <ListItem>
            {renderProgressIcon(SyncState.Metadata, SyncState.ErrorProcessing)}
            Extract metadata
          </ListItem>
          <ListItem>
            {renderProgressIcon(SyncState.Compress, SyncState.ErrorProcessing)}
            Compress audio
          </ListItem>
          <ListItem>
            {renderProgressIcon(SyncState.Hashses, SyncState.ErrorProcessing)}
            Generate hashes
          </ListItem>
          <ListItem>
            {renderProgressIcon(SyncState.SettingCuePoints, SyncState.ErrorSettingCuePoints)}
            Set cue points
          </ListItem>
        </>
        )}
      </List>
      {errorText && (
        <Button
          color="error"
          onClick={returnToPrevious}
          variant="contained"
        >
          <ArrowBack />
          Back
        </Button>
      )}
      {state === SyncState.Complete && (
        <Button
          onClick={goForward}
          variant="contained"
        >
          <ArrowForward />
          Edit Cart
        </Button>
      )}
    </>
  );
};

export default CartSynchroniser;
