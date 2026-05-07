import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Article, SourceResponse, ArticlesResponse } from "../models/article.model";

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
}