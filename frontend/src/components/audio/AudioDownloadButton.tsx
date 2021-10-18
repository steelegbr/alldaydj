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
    <Snackbar autoHideDuration={6000} onClose={clearError} open={error}>
      <Alert severity="error">Failed to download the cart audio.</Alert>
    </Snackbar>
  );

  if (downloadType === 'Compressed') {
    return (
      <>
        {error && generateError()}
        <Button aria-controls="download compressed audio" onClick={getAudioInfo}>
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
      <Button aria-controls="download linear audio" onClick={getAudioInfo}>
        <GetApp />
        {' '}
        Linear (WAV)
      </Button>
    </>
  );
};

export default AudioDownloadButton;
