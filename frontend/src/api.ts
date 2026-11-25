import type { Assessment, Course, Dashboard, QuizResult, TeachingSession } from './types';

const BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');
export const json = (value: unknown): Pick<RequestInit, 'body' | 'headers'> => ({ body: JSON.stringify(value), headers: { 'Content-Type': 'application/json' } });

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try { response = await fetch(`${BASE_URL}${path.startsWith('/') ? path : `/${path}`}`, init); }
  catch { throw new Error('Can’t reach ExamPilot. Check that the backend is running and try again.'); }
  if (!response.ok) {
    let message = `Request failed (${response.status}).`;
    try { const body: unknown = await response.json(); if (typeof body === 'object' && body !== null && 'detail' in body) { const detail = (body as { detail: unknown }).detail; message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map(String).join(', ') : message; } } catch { /* Response body was not JSON. */ }
    throw new Error(message);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

// Keep HTTP details centralized and aligned with backend/app/api/routes.
export const coursesApi = {
  list: () => api<Course[]>('/courses'),
  get: (id: string) => api<Course>(`/courses/${encodeURIComponent(id)}`),
  upload: (form: FormData) => api<Course>('/courses/upload', { method: 'POST', body: form }),
  remove: (id: string) => api<{ deleted: boolean }>(`/courses/${encodeURIComponent(id)}`, { method: 'DELETE' }),
  dashboard: () => api<Dashboard>('/dashboard'),
  startDiagnostic: (id: string) => api<Assessment>(`/courses/${encodeURIComponent(id)}/diagnostic`, { method: 'POST' }),
};
export const assessmentApi = {
  getDiagnostic: (id: string) => api<Assessment>(`/diagnostics/${encodeURIComponent(id)}`),
  answerDiagnostic: (id: string, questionId: string, answer: string) => api<{ saved: boolean; completed: boolean; results: QuizResult | null }>(`/diagnostics/${encodeURIComponent(id)}/answer`, { method: 'POST', ...json({ question_id: questionId, answer }) }),
  createExam: (courseId: string, count = 8) => api<Assessment>(`/exams/course/${encodeURIComponent(courseId)}`, { method: 'POST', ...json({ count }) }),
  getExam: (id: string) => api<Assessment>(`/exams/${encodeURIComponent(id)}`),
  submitExam: (id: string, answers: Record<string, string>) => api<QuizResult>(`/exams/${encodeURIComponent(id)}/submit`, { method: 'POST', ...json({ answers }) }),
};
export const teachingApi = {
  create: (courseId: string, conceptId: string) => api<TeachingSession>('/teaching-sessions', { method: 'POST', ...json({ course_id: courseId, concept_id: conceptId }) }),
  advance: (id: string) => api<TeachingSession>(`/teaching-sessions/${encodeURIComponent(id)}/advance`, { method: 'POST' }),
  check: (id: string, answer: string) => api<{ received: boolean; feedback: string }>(`/teaching-sessions/${encodeURIComponent(id)}/check`, { method: 'POST', ...json({ answer: { text: answer } }) }),
};
