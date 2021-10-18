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

import { GetApp } from '@mui/icons-material';
import { Alert, Button, Snackbar } from '@mui/material';
import { CartAudio } from 'api/models/Cart';
import { getCartAudio } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import React from 'react';
import { getLogger } from 'services/LoggingService';

export type DownloadType = 'Compressed' | 'Linear';

interface AudioDownloadButtonProps {
    cartId: string,
    label: string,
    downloadType: DownloadType
}

const AudioDownloadButton = (props: AudioDownloadButtonProps): React.ReactElement => {
  const { cartId, downloadType, label } = props;
  const authenticationContext = React.useContext(AuthenticationContext);
  const [error, setError] = React.useState<boolean>(false);

  const token = authenticationContext?.authenticationStatus.accessToken;

  const clearError = () => {
    setError(false);
  };

  const triggerDownload = React.useCallback(
    (cartAudio: CartAudio) => {
      const url = downloadType === 'Compressed' ? cartAudio.compressed : cartAudio.audio;
      const fileName = downloadType === 'Compressed' ? `${label}.ogg` : `${label}.wav`;
      if (url) {
        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.download = fileName;
        downloadLink.target = '_blank';
        downloadLink.click();
        getLogger().info(`Triggered download from ${url} for ${fileName}`);
      } else {
        getLogger().error(`Failed to obtain download URL for cart ${label}`);
        setError(true);
      }
    },
    [downloadType, label],
  );

  const getAudioInfo = React.useCallback(
    () => {
      if (token) {
        getLogger().info(`Attempting to get audio info for cart ID ${cartId}`);
        getCartAudio(cartId, token).then(
          (response: AxiosResponse<CartAudio>) => {
            if (response.status === 200) {
              getLogger().info('Successfully obtained cart audio info.');
              triggerDownload(response.data);
            } else {
              getLogger().error(response);
              getLogger().error(`Got a strange HTTP response (${response.status}) getting cart audio info.`);
              setError(true);
            }
          },
          (errorResponse) => {
            getLogger().error(`Failed to download the cart audio: ${errorResponse}`);
            setError(true);
          },
        );
      }
    },
    [cartId, token, triggerDownload],
  );

  const generateError = () => (
    <Snackbar autoHideDuration={6000} data-test="download-error" onClose={clearError} open={error}>
      <Alert severity="error">Failed to download the cart audio.</Alert>
    </Snackbar>
  );

  if (downloadType === 'Compressed') {
    return (
      <>
        {error && generateError()}
        <Button aria-controls="download compressed audio" data-test="button-download-compressed" onClick={getAudioInfo}>
          <GetApp />
          {' '}
          Compressed (OGG)
        </Button>
      </>
    );
  }

  return (
    <>
      {error && generateError()}
      <Button aria-controls="download linear audio" data-test="button-download-linear" onClick={getAudioInfo}>
        <GetApp />
        {' '}
        Linear (WAV)
      </Button>
    </>
  );
};

export default AudioDownloadButton;
