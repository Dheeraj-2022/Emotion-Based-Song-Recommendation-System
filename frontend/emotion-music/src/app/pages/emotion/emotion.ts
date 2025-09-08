import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import * as faceapi from 'face-api.js';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-emotion',
  standalone: true,
  imports: [CommonModule, MatToolbarModule, MatButtonModule, MatCardModule],
  templateUrl: './emotion.html',
  styleUrls: ['./emotion.scss'],
})
export class EmotionComponent implements OnInit, OnDestroy {
  video!: HTMLVideoElement;
  emotion: string = 'neutral';
  interval: any;

  constructor(private router: Router) {}

  async ngOnInit(): Promise<void> {
    await this.loadModels();
    this.startVideo();
  }

  ngOnDestroy(): void {
    if (this.interval) clearInterval(this.interval);
    if (this.video && this.video.srcObject) {
      (this.video.srcObject as MediaStream).getTracks().forEach(track => track.stop());
    }
  }

  async loadModels(): Promise<void> {
    await faceapi.nets.tinyFaceDetector.loadFromUri('/assets/models');
    await faceapi.nets.faceExpressionNet.loadFromUri('/assets/models');
  }

  async startVideo(): Promise<void> {
    this.video = document.querySelector('video')!;
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      this.video.srcObject = stream;
    });

    this.video.addEventListener('play', () => {
      this.interval = setInterval(async () => {
        const detections = await faceapi
          .detectSingleFace(this.video, new faceapi.TinyFaceDetectorOptions())
          .withFaceExpressions();
        if (detections && detections.expressions) {
          this.emotion = Object.keys(detections.expressions).reduce((a, b) =>
            detections.expressions[a]! > detections.expressions[b]! ? a : b
          );
        }
      }, 700);
    });
  }

  goToSongs(): void {
    this.router.navigate(['/recommendations'], { queryParams: { emotion: this.emotion } });
  }
}
