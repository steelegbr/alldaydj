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
  CheckBox, CheckBoxOutlineBlank, Error,
} from '@mui/icons-material';
import {
  Alert,
  Button,
  CircularProgress, List, ListItem, Typography,
} from '@mui/material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
import { AudioUploadJob, Cart } from 'api/models/Cart';
import { createCart, updateCart, uploadAudio } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import React from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import { getLogger } from 'services/LoggingService';

const ERROR_UPLOAD_AUDIO = 'Something went wrong uploading the audio. Please try again later.';
const ERROR_UPDATE_CART = 'Something went wrong updating the cart. Please try again later.';

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

const CartSynchroniser = (): React.ReactElement => {
  const history = useHistory();
  const classes = useStyles();
  const location = useLocation<CartSynchroniserState>();
  const { cart, file } = location.state;
  const [state, setState] = React.useState<SyncState>(SyncState.Idle);
  const [errorText, setErrorText] = React.useState<string>();
  const [updatedCart, setUpdatedCart] = React.useState<Cart>(cart);
  const [uploadProgress, setUploadProgress] = React.useState<number>(0);

  const renderToDo = () => (<CheckBoxOutlineBlank />);
  const renderError = () => (<Error color="error" />);
  const renderSuccess = () => (<CheckBox color="success" />);
  const renderProgress = () => (<CircularProgress className={classes.spinner} />);

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
      if (response.status === 200) {
        setUpdatedCart(response.data);
        if (file) {
          setState(SyncState.UploadingAudio);
          uploadAudio(cart, file, progressCallback).then(uploadAudioSuccess, uploadAudioError);
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
          {state === SyncState.Idle && (
            renderToDo()
          )}
          {state === SyncState.UpdatingCart && (
            renderProgress()
          )}
          {state === SyncState.ErrorUpdatingCart && (
            renderError()
          )}
          {state > SyncState.ErrorUpdatingCart && (
            renderSuccess()
          )}
          {cart.id ? 'Update Cart' : 'Upload New Cart'}
        </ListItem>
        {file && (
        <>
          <ListItem>
            {state < SyncState.UploadingAudio && (
              renderToDo()
            )}
            {state === SyncState.UploadingAudio && uploadProgress < 100 && (
              <CircularProgress className={classes.spinner} value={uploadProgress} variant="determinate" />
            )}
            {state === SyncState.UploadingAudio && uploadProgress === 100 && (
              renderProgress()
            )}
            {state === SyncState.ErrorUploadingAudio && (
              renderError()
            )}
            {state > SyncState.Queued && (
              renderSuccess()
            )}
            Upload audio
          </ListItem>
          <ListItem>
            {renderToDo()}
            Validate audio file
          </ListItem>
          <ListItem>
            <CheckBoxOutlineBlank />
            Decompress audio file
          </ListItem>
          <ListItem>
            Extract metadata
          </ListItem>
          <ListItem>
            Compress audio
          </ListItem>
          <ListItem>
            Generate hashes
          </ListItem>
          <ListItem>
            Set cue points (
            {updatedCart.id}
            )
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
    </>
  );
};

export default CartSynchroniser;
