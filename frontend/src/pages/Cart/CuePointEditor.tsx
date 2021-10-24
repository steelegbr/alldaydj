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

import { Button, Grid } from '@mui/material';
import { Cart } from 'api/models/Cart';
import { CartEditorContext } from 'components/context/CartEditorContext';
import React from 'react';
import { millisecondToMinutesSecondMilliseconds } from 'services/TimeService';

export enum CuePoint {
    Start,
    IntroEnd,
    Segue,
    End
}

interface CuePointEditorProps {
    cuePoint: CuePoint
}

const backgroundColourMap = new Map<CuePoint, string>([
  [CuePoint.Start, '#000000'],
  [CuePoint.IntroEnd, '#00FF00'],
  [CuePoint.Segue, '#FFFF00'],
  [CuePoint.End, '#000000'],
]);

const colourMap = new Map<CuePoint, string>([
  [CuePoint.Start, '#FFFFFF'],
  [CuePoint.IntroEnd, '#000000'],
  [CuePoint.Segue, '#000000'],
  [CuePoint.End, '#FFFFFF'],
]);

const labelMap = new Map<CuePoint, string>([
  [CuePoint.Start, 'Start'],
  [CuePoint.IntroEnd, 'Intro'],
  [CuePoint.Segue, 'Segue'],
  [CuePoint.End, 'End'],
]);

const getCuePointValue = (cart: Cart | undefined, cuePoint: CuePoint) => {
  switch (cuePoint) {
    case CuePoint.Start:
      return cart?.cue_audio_start;
    case CuePoint.IntroEnd:
      return cart?.cue_intro_end;
    case CuePoint.Segue:
      return cart?.cue_segue;
    default:
      return cart?.cue_audio_end;
  }
};

const valueToDisplay = (value: number | undefined) => {
  if (value !== undefined) {
    return millisecondToMinutesSecondMilliseconds(value);
  }
  return '0:00.0';
};

const CuePointEditor = ({ cuePoint }: CuePointEditorProps): React.ReactElement => {
  const { cart } = React.useContext(CartEditorContext);
  const value = getCuePointValue(cart, cuePoint);
  const colour = colourMap.get(cuePoint);
  const backgroundColour = backgroundColourMap.get(cuePoint);
  const label = labelMap.get(cuePoint);

  return (
    <Grid container direction="column" justifyContent="center" xs={3}>
      <Grid item>
        <Button fullWidth style={{ color: colour, backgroundColor: backgroundColour }}>
          {`Set ${label}`}
        </Button>
      </Grid>
      <Grid item>
        {valueToDisplay(value)}
      </Grid>
      <Grid item>
        <Button fullWidth style={{ color: colour, backgroundColor: backgroundColour }}>
          {`Cue ${label}`}
        </Button>
      </Grid>
    </Grid>
  );
};

export default CuePointEditor;
