import { useState } from 'react';
import { ArrowLeft, ArrowRight, BookOpen, CircleHelp, LoaderCircle } from 'lucide-react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { assessmentApi } from '../api';
import { LoadingState, Notice, EmptyState } from '../components/States';
import { useResource } from '../hooks/useResource';
import type { Course } from '../types';

export function CoursePage() {
  const { id = '' } = useParams(); const { data: course, error, loading } = useResource<Course>(`/courses/${encodeURIComponent(id)}`);
  const [busy, setBusy] = useState(''); const [actionError, setActionError] = useState(''); const navigate = useNavigate();
  async function diagnostic() { setBusy('diagnostic'); setActionError(''); try { const result = await assessmentApi.startDiagnostic(id); navigate(`/diagnostic/${result.id}`); } catch (cause) { setActionError(cause instanceof Error ? cause.message : 'Could not start knowledge check.'); } finally { setBusy(''); } }
  async function exam() { setBusy('exam'); setActionError(''); try { const result = await assessmentApi.createExam(id); navigate(`/exam/${result.id}`); } catch (cause) { setActionError(cause instanceof Error ? cause.message : 'Could not create practice exam.'); } finally { setBusy(''); } }
  if (loading) return <LoadingState label="Loading course…" />;
  if (error || !course) return <><Notice error>{error || 'Course not found.'}</Notice><Link to="/" className="back-link"><ArrowLeft size={16} /> Back to library</Link></>;
  const chapters = course.knowledge_map?.chapters ?? [];
  return <><Link to="/" className="back-link"><ArrowLeft size={16} /> Your library</Link><section className="course-hero"><div className="eyebrow"><BookOpen size={14} /> COURSE WORKSPACE</div><h1>{course.title}</h1><p>{course.description || 'Explore your course materials, build understanding, and check your progress.'}</p><div className="hero-actions"><button className="button button-primary" onClick={() => void diagnostic()} disabled={!!busy || course.status !== 'ready'}>{busy === 'diagnostic' ? <LoaderCircle className="spin" size={17} /> : null}Start knowledge check</button><button className="button button-secondary" onClick={() => void exam()} disabled={!!busy || course.status !== 'ready'}>{busy === 'exam' ? <LoaderCircle className="spin" size={17} /> : <CircleHelp size={17} />}Practice exam</button></div></section>
    {actionError && <Notice error>{actionError}</Notice>}
    <section className="section-block"><div className="section-heading"><div><span className="eyebrow">THE BIG PICTURE</span><h2>Course knowledge map</h2></div><span className="count-pill">{chapters.length} chapters</span></div>
      {chapters.length ? <div className="chapter-list">{chapters.map((chapter, i) => <article className="chapter-card" key={`${chapter.title}-${i}`}><div className="chapter-number">{String(i + 1).padStart(2, '0')}</div><div className="chapter-body"><h3>{chapter.title}</h3>{chapter.description && <p>{chapter.description}</p>}<div className="concept-list">{(chapter.concepts ?? []).map((concept, j) => <div className="concept-row" key={`${concept.name}-${j}`}><div><strong>{concept.name}</strong>{concept.definition && <p>{concept.definition}</p>}</div><Link className="text-action" to={`/learn/${encodeURIComponent(id)}/${encodeURIComponent(concept.id ?? concept.name)}`}>Learn this <ArrowRight size={14} /></Link></div>)}</div></div></article>)}</div> : <EmptyState title="We’re preparing your course map">When course analysis is complete, the key chapters and concepts will appear here.</EmptyState>}
    </section></>;
}
