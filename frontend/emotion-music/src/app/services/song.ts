import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SongService {
  constructor() {}

  getSongsForEmotion(emotion: string) {
    switch (emotion.toLowerCase()) {
      case 'happy':
        return [
          { title: 'Happy Song 1', artist: 'Artist 1', image: 'assets/images/happy1.jpg' },
          { title: 'Happy Song 2', artist: 'Artist 2', image: 'assets/images/happy2.jpg' },
        ];
      case 'sad':
        return [
          { title: 'Sad Song 1', artist: 'Artist 3', image: 'assets/images/sad1.jpg' },
          { title: 'Sad Song 2', artist: 'Artist 4', image: 'assets/images/sad2.jpg' },
        ];
      case 'angry':
        return [
          { title: 'Angry Song 1', artist: 'Artist 5', image: 'assets/images/angry1.jpg' },
        ];
      default:
        return [
          { title: 'Neutral Song', artist: 'Artist 6', image: 'assets/images/neutral.jpg' },
        ];
    }
  }
}
