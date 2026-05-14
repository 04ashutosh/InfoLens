import { Component,OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { NewsService } from "../../services/news.service";
import { 
  SourceInfo, Article, DailyBriefResponse, 
  BiasAnalysisResponse, SimilarArticlesResponse
} from "../../models/article.model";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})

export class Dashboard implements OnInit{
  healthStatus: string = 'Checking...';
  isLoading: boolean = true;

  articles: Article[] = []

  // AI State Variables
  dailyBrief: DailyBriefResponse | null = null;
  isFetchingNews = false;
  isGeneratingBrief = false;

  // Dictionaries to store results for specific articles
  biasResults: {[id: number]: BiasAnalysisResponse} = {};
  similarResults: {[id: number]: SimilarArticlesResponse} = {};
  analyzingBias: {[id: number]: boolean} = {};
  findingSimilar: {[id: number]: boolean} = {};

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.loadHealth();
    this.loadArticles();
  }

  loadHealth(): void {
    this.newsService.checkHealth().subscribe({
      next: (data)=> this.healthStatus = data.status,
      error: () => this.healthStatus = 'Offline'
    });
  }

  loadArticles(): void {
    this.isLoading = true;
    this.newsService.getArticles().subscribe({
      next: (data) => {
        this.articles = data.articles;
        this.isLoading = false;
      },
      error: () => this.isLoading = false
    });
  }

  // ---NEW AI ACTION METHODS ---

  triggerNewsFetch(): void {
    this.isFetchingNews = true;
    this.newsService.triggerFetch().subscribe({
      next: (res) => {
        alert(res.message);
        this.loadArticles(); // Reload this list
        this.isFetchingNews = false;
      },
      error: () => this.isFetchingNews = false
    });
  }

  generateDailyBrief(): void{
    this.isGeneratingBrief = true;
    this.newsService.getDailyBrief().subscribe({
      next: (res) => {
        this.dailyBrief = res;
        this.isGeneratingBrief = false;
      },
      error: ()=> this.isGeneratingBrief = false
    });
  }

  analyzeBias(articleId: number): void {
    this.analyzingBias = { ...this.analyzingBias, [articleId]: true };
    this.newsService.getArticleBias(articleId).subscribe({
      next: (res) => {
        this.biasResults = { ...this.biasResults, [articleId]: res };
        this.analyzingBias = { ...this.analyzingBias, [articleId]: false };
      },
      error: () => {
        this.analyzingBias = { ...this.analyzingBias, [articleId]: false };
      }
    });
  }

  findSimilar(articleId: number): void {
    this.findingSimilar = { ...this.findingSimilar, [articleId]: true };
    this.newsService.getSimilarArticles(articleId).subscribe({
      next: (res)=>{
        this.similarResults = { ...this.similarResults, [articleId]: res };
        this.findingSimilar = { ...this.findingSimilar, [articleId]: false };
      },
      error: ()=> {
        this.findingSimilar = { ...this.findingSimilar, [articleId]: false };
      }
    });
  }
}