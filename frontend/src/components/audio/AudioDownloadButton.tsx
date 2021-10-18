import { GetApp } from '@mui/icons-material';
import { Button } from '@mui/material';
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
  const token = authenticationContext?.authenticationStatus.accessToken;

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
          (error) => {
            getLogger().error(`Failed to download the cart audio: ${error}`);
          },
        );
      }
    },
    [cartId, token, triggerDownload],
  );

  if (downloadType === 'Compressed') {
    return (
      <Button aria-controls="download compressed audio" onClick={getAudioInfo}>
        <GetApp />
        {' '}
        Compressed (OGG)
      </Button>
    );
  }

  return (
    <Button aria-controls="download linear audio" onClick={getAudioInfo}>
      <GetApp />
      {' '}
      Linear (WAV)
    </Button>
  );
};

export default AudioDownloadButton;
