import {
  Event, Label, LibraryMusic, People, Person,
} from '@mui/icons-material';
import {
  Alert,
  Checkbox,
  CircularProgress,
  FormControl,
  FormControlLabel,
  FormGroup,
  Grid,
  InputAdornment,
  TextField,
} from '@mui/material';
import { Cart } from 'api/models/Cart';
import { getCartDetails } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import CartTypeSelector from 'components/audio/CartTypeSelector';
import TagChips from 'components/audio/TagChips';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import React from 'react';
import { useParams } from 'react-router-dom';
import { getLogger } from 'services/LoggingService';
import { CartFields, MAX_PERMITTED_YEAR, validateCart } from 'services/ValidationService';

type EditorState = 'Loading' | 'Error' | 'Loaded';
type CartEditorParams = {
    cartId: string
}

const CartEditor = (): React.ReactElement => {
  const { cartId } = useParams<CartEditorParams>();
  const [cart, setCart] = React.useState<Cart>();
  const [editorState, setEditorState] = React.useState<EditorState>('Loading');
  const authenticatonContext = React.useContext(AuthenticationContext);
  const token = authenticatonContext?.authenticationStatus.accessToken;
  const validationErrors = validateCart(cart);

  React.useEffect(
    () => {
      if (cartId && token) {
        getLogger().info(`Downloading cart ${cartId} information for editing.`);
        setEditorState('Loading');
        getCartDetails(cartId, token).then(
          (response: AxiosResponse<Cart>) => {
            if (response.status === 200) {
              setCart(response.data);
              setEditorState('Loaded');
            } else {
              getLogger().error(`Got HTTP response code ${response.status}.`);
              setEditorState('Error');
            }
          },
          (error) => {
            getLogger().error(`Something went wrong loading the cart for editing: ${error}`);
            setEditorState('Error');
          },
        );
      }
    },
    [cartId, token],
  );

  const updateLabel = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          label: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateDisplayArtist = React.useCallback(
    (
      event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>,
    ) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          display_artist: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateTitle = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          title: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateYear = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          year: Number.parseInt(event.target.value, 10),
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateISRC = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          isrc: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateRecordLabel = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          record_label: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateComposer = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          composer: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updatePublisher = React.useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          publisher: event.target.value,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const toggleSweeper = React.useCallback(
    () => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          sweeper: !cart.sweeper,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const toggleFade = React.useCallback(
    () => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          fade: !cart.fade,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateType = React.useCallback(
    (newType: string) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          type: newType,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  const updateTags = React.useCallback(
    (tags: string[]) => {
      if (cart) {
        const updatedCart: Cart = {
          ...cart,
          tags,
        };
        setCart(updatedCart);
      }
    },
    [cart],
  );

  if (editorState === 'Loading') {
    return (
      <Grid alignItems="center" container justifyContent="space-between">
        <Grid item xs={12}>
          <CircularProgress />
        </Grid>
        <Grid item>
          Loading cart... it&apos;ll be just a moment...
        </Grid>
      </Grid>
    );
  }

  if (editorState === 'Error' || !cart) {
    return (
      <Alert severity="error">Something went wrong. Please try again later.</Alert>
    );
  }

  return (
    <form data-test="form-cart-editor">
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Label />
            </InputAdornment>
          ),
        }}
        data-test="input-label"
        error={validationErrors.includes(CartFields.Label)}
        fullWidth
        helperText={validationErrors.includes(CartFields.Label) ? 'You must supplied a label / cart number consisting of only letters and numbers.' : undefined}
        id="label"
        label="Label:"
        margin="normal"
        onChange={(event) => { updateLabel(event); }}
        required
        value={cart.label}
        variant="standard"
      />
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Person />
            </InputAdornment>
          ),
        }}
        data-test="input-display-artist"
        fullWidth
        id="display-artist"
        label="Artist:"
        margin="normal"
        onChange={updateDisplayArtist}
        value={cart.display_artist}
        variant="standard"
      />
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <LibraryMusic />
            </InputAdornment>
          ),
        }}
        data-test="input-title"
        error={validationErrors.includes(CartFields.Title)}
        fullWidth
        helperText={validationErrors.includes(CartFields.Title) ? 'You must supply a title for this cart.' : undefined}
        id="title"
        label="Title:"
        margin="normal"
        onChange={updateTitle}
        required
        value={cart.title}
        variant="standard"
      />
      <FormControl fullWidth variant="standard">
        <FormGroup>
          <FormControlLabel
            control={
              <Checkbox checked={cart.sweeper} data-test="check-sweeper" name="sweeper" />
                }
            label="Sweeper"
            onChange={toggleSweeper}
          />
          <FormControlLabel
            control={
              <Checkbox checked={cart.fade} data-test="check-fade" name="fade" />
                }
            label="Fades Out"
            onChange={toggleFade}
          />
        </FormGroup>
      </FormControl>
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Event />
            </InputAdornment>
          ),
        }}
        data-test="input-year"
        error={validationErrors.includes(CartFields.Year)}
        helperText={validationErrors.includes(CartFields.Year) ? `The year must be a number between 0 and ${MAX_PERMITTED_YEAR}.` : undefined}
        id="year"
        label="Year:"
        margin="normal"
        onChange={updateYear}
        type="number"
        value={cart.year}
        variant="standard"
      />
      <CartTypeSelector selectedType={cart.type} setSelectedType={updateType} />
      <TagChips selectedTags={cart.tags} setSelectedTags={updateTags} />
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Label />
            </InputAdornment>
          ),
        }}
        data-test="input-isrc"
        fullWidth
        id="isrc"
        label="ISRC:"
        margin="normal"
        onChange={updateISRC}
        value={cart.isrc}
        variant="standard"
      />
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <People />
            </InputAdornment>
          ),
        }}
        data-test="input-record-label"
        fullWidth
        id="record-label"
        label="Record Label:"
        margin="normal"
        onChange={updateRecordLabel}
        value={cart.record_label}
        variant="standard"
      />
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <People />
            </InputAdornment>
          ),
        }}
        data-test="input-composer"
        fullWidth
        id="composer"
        label="Composer:"
        margin="normal"
        onChange={updateComposer}
        value={cart.composer}
        variant="standard"
      />
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <People />
            </InputAdornment>
          ),
        }}
        data-test="input-publisher"
        fullWidth
        id="publisher"
        label="Publisher:"
        margin="normal"
        onChange={updatePublisher}
        value={cart.publisher}
        variant="standard"
      />
    </form>
  );
};

export default CartEditor;
