import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'Resumidor de textos';
  inputText = '';
  summary = '';

  constructor(private http: HttpClient) {}

  onSummarize() {
    this.http.post('http://localhost:8000/summarize', { text: this.inputText })
      .subscribe((response: any) => {
        this.summary = response.summary;
        console.log('Summary:', this.summary);
      });
  }
}
