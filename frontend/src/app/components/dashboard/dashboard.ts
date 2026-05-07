import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';
import { SourceInfo, SourceResponse } from '../../models/article.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {

  // Properties (like Java fields)
  sources: SourceInfo[] = [];
  healthStatus: string = 'Checking...';
  isLoading: boolean = true;

  // Constructor injection (like @Autowired in Spring)
  constructor(private newsService: NewsService) {}

  // ngOnInit = runs when component loads (like @PostConstruct in Spring)
  ngOnInit(): void {
    this.loadHealth();
    this.loadSources();
  }

  loadHealth(): void {
    this.newsService.checkHealth().subscribe({
      next: (data) => this.healthStatus = data.status,
      error: () => this.healthStatus = 'Offline'
    });
  }

  loadSources(): void {
    this.newsService.getSources().subscribe({
      next: (data) => {
        this.sources = data.sources;
        this.isLoading = false;
      },
      error: () => this.isLoading = false
    });
  }
}
