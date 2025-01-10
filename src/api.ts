export interface Email {
    id: string;
    sender: string;
    subject: string;
    snippet: string;
    body: string;
    sentimentScore: number;
    category: string;
    keywords: string[];
    prologMatches: string[];
  }
  