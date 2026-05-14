export interface Article{
    id?: number;
    title: string;
    source: string;
    content: string;
    category: string;
}

export interface SourceInfo{
    name: string;
    category: string;
}

export interface SourceResponse{
    sources : SourceInfo[];
    count: number;
}

export interface ArticlesResponse{
    articles: Article[];
    total: number;
}

// AI Responses

export interface DailyBriefResponse{
    sources_used: string[];
    titles_analyzed: string[];
    daily_brief: string
}

export interface BiasAnalysis{
    bias_rating: string;
    reasoning: string;
    emotional_tone: string;
}

export interface BiasAnalysisResponse{
    article_id: number;
    title: string;
    analysis: BiasAnalysis;
}

export interface SimilarArticle{
    id: number;
    title: string;
    source: string;
    similarity_score: number;
}

export interface SimilarArticlesResponse{
    target_id: number;
    threshold: number;
    similar_articles: SimilarArticle[];
}