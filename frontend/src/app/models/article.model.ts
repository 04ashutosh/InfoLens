export interface Article{
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