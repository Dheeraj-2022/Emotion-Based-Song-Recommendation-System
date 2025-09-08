import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SongService } from '../../services/song';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-recommendations',
  standalone: true,
  imports: [CommonModule, MatToolbarModule, MatCardModule, MatButtonModule],
  templateUrl: './recommendations.html',
  styleUrls: ['./recommendations.scss'],
})
export class RecommendationsComponent implements OnInit {
  emotion: string = 'neutral';
  songs: { title: string; artist: string; image: string }[] = [];

  constructor(private route: ActivatedRoute, private songService: SongService) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.emotion = params['emotion'] || 'neutral';
      this.songs = this.songService.getSongsForEmotion(this.emotion);
    });
  }
}
