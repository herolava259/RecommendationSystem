export interface MovieCard {
  title: string;
  rating: number;
  votes?: number;
  viewCount?: number;
  year: number;
  genres: string[];
  posterUrl: string;
  duration: string;
  description: string;
  imdbScore: number;
}

