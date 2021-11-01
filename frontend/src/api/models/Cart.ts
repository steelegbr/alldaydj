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

export interface Cart {
    id: string;
    label: string;
    title: string;
    display_artist: string,
    cue_audio_start: number,
    cue_audio_end: number,
    cue_intro_end: number,
    cue_segue: number
    artists: string[],
    sweeper: boolean,
    year: number,
    isrc: string,
    composer: string,
    publisher: string,
    record_label: string,
    tags: string[],
    type: string,
    fade: boolean
}

export interface CartAudio {
    audio: string;
    compressed: string;
    hash_audio: string;
    hash_compressed: string;
}

export interface CartType {
    id: string,
    name: string,
    colour: string,
    now_playing: boolean
}

export interface Tag {
    id: string,
    tag: string
}

export type AudioJobStatus = 'QUEUED' | 'ERROR' | 'VALIDATING' | 'DECOMPRESSING' | 'METADATA' | 'COMPRESSING' | 'HASHING' | 'DONE';
export interface AudioUploadJob {
    id: string,
    status: AudioJobStatus
}

export interface Sequencer {
    id: string,
    name: string
}

export interface SequencerNext {
    next: string
}
