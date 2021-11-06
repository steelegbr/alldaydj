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

import { DeleteForever } from '@mui/icons-material';
import {
  Alert,
  Button,
  Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Snackbar,
} from '@mui/material';
import { Cart } from 'api/models/Cart';
import { deleteCart } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import React from 'react';
import { getLogger } from 'services/LoggingService';

interface CartDeleteAlertProps {
    cart: Cart
    onDelete: () => void,
    onCancel: () => void
}

const CartDeleteAlert = (
  { cart, onDelete, onCancel }: CartDeleteAlertProps,
) => {
  const [error, setError] = React.useState<boolean>(false);

  const handleDelete = React.useCallback(
    () => {
      deleteCart(cart).then(
        (response: AxiosResponse<Cart>) => {
          if (response.status === 204) {
            setError(false);
            onDelete();
          } else {
            getLogger().error(`Got status code ${response.status} trying to delete the cart.`);
            setError(true);
          }
        },
        (deleteError: Error) => {
          getLogger().error(`Got an error trying to delete the cart: ${deleteError}`);
          setError(true);
        },
      );
    },
    [cart, onDelete],
  );

  const clearError = React.useCallback(
    () => {
      setError(false);
    },
    [setError],
  );

  return (
    <>
      <Snackbar autoHideDuration={6000} onClose={clearError} open={error}>
        <Alert data-test="error" severity="error">Something went wrong attempting to delete the cart. Please try again later.</Alert>
      </Snackbar>
      <Dialog
        aria-describedby="alert-cart-delete-description"
        aria-labelledby="alert-cart-delete-title"
        onClose={onCancel}
        open
      >
        <DialogTitle id="alert-cart-delete-title">
          {`Delete ${cart.label}?`}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-cart-delete-description">
            Deleting a cart also deletes the audio and an irrevocable action.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button
            color="error"
            data-test="alert-button-delete"
            onClick={handleDelete}
            variant="contained"
          >
            <DeleteForever />
            Delete
          </Button>
          <Button
            color="secondary"
            data-test="alert-button-cancel"
            onClick={onCancel}
            variant="contained"
          >
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default CartDeleteAlert;
