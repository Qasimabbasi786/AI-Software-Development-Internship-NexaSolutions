export interface Author {
  authorId: number;
  fullName: string;
  city?: string;
  email?: string;
}

export interface Book {
  bookId?: number;
  id?: number;
  title: string;
  authorId?: number;
  author?: Author | string;
  isbn?: string;
  publicationYear?: number;
  category?: string;
  createdAt?: string;
}