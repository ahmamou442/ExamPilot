import type { ReactNode } from 'react';
import { LoaderCircle } from 'lucide-react';

export function LoadingState({ label = 'Loading…' }: { label?: string }) { return <div className="loading" role="status"><LoaderCircle className="spin" size={22} />{label}</div>; }
export function Notice({ children, error = false }: { children: ReactNode; error?: boolean }) { return <div className={`notice${error ? ' error' : ''}`} role={error ? 'alert' : 'status'}>{children}</div>; }
export function EmptyState({ title, children }: { title: string; children: ReactNode }) { return <section className="empty-state"><h3>{title}</h3><p>{children}</p></section>; }
