import {
  Button, Menu, MenuItem, TableCell, TableRow,
} from '@material-ui/core';
import { GetApp, PlayArrow } from '@material-ui/icons';
import React from 'react';
import { CartSearchResult } from '../../api/models/Search';

interface TableRowProps {
    result: CartSearchResult
}

const LibraryTableRow = ({ result }: TableRowProps) => {
  const [anchorButton, setAnchorButton] = React.useState<HTMLElement | undefined>(undefined);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorButton(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorButton(undefined);
  };

  return (
    <TableRow>
      <TableCell>{result.label}</TableCell>
      <TableCell>{result.artist}</TableCell>
      <TableCell>{result.title}</TableCell>
      <TableCell>
        <Button aria-controls="download audio" aria-haspopup="true" onClick={handleClick}>
          <GetApp />
        </Button>
        <Menu
          anchorEl={anchorButton}
          id="menu-audio-download"
          keepMounted
          onClose={handleClose}
          open={Boolean(anchorButton)}
        >
          <MenuItem onClick={handleClose}>Compressed (OGG)</MenuItem>
          <MenuItem onClick={handleClose}>Uncompressed (WAV)</MenuItem>
        </Menu>
      </TableCell>
      <TableCell>
        <Button>
          <PlayArrow />
        </Button>
      </TableCell>
    </TableRow>
  );
};

export default LibraryTableRow;
