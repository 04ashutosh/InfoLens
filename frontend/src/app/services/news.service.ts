import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Article, SourceResponse, ArticlesResponse, DailyBriefResponse, SimilarArticlesResponse, BiasAnalysisResponse } from "../models/article.model";

@Injectable({
    providedIn: 'root' // Like @Service - available everywhere
})

export class NewsService{
    // Base URL of our Python FastAPI server
    private apiUrl = 'http://localhost:8000';

    constructor(private http: HttpClient) {}

    //GET /api/sources
    getSources(): Observable<SourceResponse>{
        return this.http.get<SourceResponse>(`${this.apiUrl}/api/sources`);
    }

    //GET /api/articles
    getArticles(): Observable<ArticlesResponse> {
        return this.http.get<ArticlesResponse>(`${this.apiUrl}/api/articles`);
    }

    //POST /api/articles
    addArticle(article: Article): Observable<any>{
        return this.http.post(`${this.apiUrl}/api/articles`,article);
    }

    //GET /health
    checkHealth(): Observable<any>{
        return this.http.get(`${this.apiUrl}/health`);
    }

    // POST /api/articles/fetch-latest
    triggerFetch(): Observable<{message: string}>{
        return this.http.post<{message: string}>(`${this.apiUrl}/api/articles/fetch-latest`,{});
    }

    // GET /api/daily-brief
    getDailyBrief(): Observable<DailyBriefResponse> {
        return this.http.get<DailyBriefResponse>(`${this.apiUrl}/api/daily-brief`);
    }

    //GET /api/articles/{article_id}/similar
    getSimilarArticles(articleId: number, threshold: number = 0.8):
    Observable<SimilarArticlesResponse>{
        return this.http.get<SimilarArticlesResponse>(`${this.apiUrl}/api/articles/${articleId}/similar?threshold=${threshold}`);
    }

    // GET /api/articles/{article_id}/bias
    getArticleBias(articleId: number): Observable<BiasAnalysisResponse>{
        return this.http.get<BiasAnalysisResponse>(`${this.apiUrl}/api/articles/${articleId}/bias`);
    }
}