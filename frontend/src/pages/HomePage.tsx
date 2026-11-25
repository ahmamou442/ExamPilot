import { FormEvent, useState } from 'react';
import { ArrowRight, Check, LoaderCircle, Plus, Sparkles, Target, UploadCloud } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { coursesApi } from '../api';
import { CourseCard } from '../components/CourseCard';
import { EmptyState, LoadingState, Notice } from '../components/States';
import { useCourses } from '../hooks/useCourses';
import type { Course } from '../types';

export function HomePage() {
  const { courses, dashboard, loading, error, setError, refresh } = useCourses();
  const [files, setFiles] = useState<File[]>([]); const [title, setTitle] = useState(''); const [busy, setBusy] = useState(false); const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const readyCount = courses.filter((course) => course.status === 'ready').length;
  const conceptsCount = dashboard?.courses.reduce((sum, course) => sum + (course.concepts_count || 0), 0) ?? 0;
  async function upload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setMessage('');
    if (!files.length) { setError('Choose at least one PDF to get started.'); return; }
    const form = new FormData(); files.forEach((file) => form.append('files', file)); if (title.trim()) form.append('title', title.trim());
    setBusy(true);
    try { const course = await coursesApi.upload(form); setFiles([]); setTitle(''); setMessage('Course uploaded and analyzed successfully.'); await refresh(); navigate(`/courses/${course.id}`); }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'Upload failed. Please try again.'); }
    finally { setBusy(false); }
  }
  async function remove(course: Course) { if (!window.confirm(`Delete “${course.title}” and its study data?`)) return; try { await coursesApi.remove(course.id); await refresh(); } catch (cause) { setError(cause instanceof Error ? cause.message : 'Could not delete the course.'); } }
  return <>
    <section className="welcome-row"><div><div className="eyebrow"><Sparkles size={14} /> YOUR NEXT BIG IDEA STARTS HERE</div><h1>Make learning <span>click.</span></h1><p className="intro">Turn your course materials into a clear, personal path to understanding.</p></div><div className="date-chip"><i className="date-dot" /> Your learning journey</div></section>
    <section className="stats-grid" aria-label="Learning overview"><Stat icon={<BookOpenIcon />} label="Your courses" value={courses.length} tone="lavender" /><Stat icon={<Check size={18} />} label="Ready to study" value={readyCount} tone="mint" /><Stat icon={<Target size={18} />} label="Concepts mapped" value={conceptsCount} tone="peach" /></section>
    {error && <Notice error>{error}</Notice>}{message && <Notice>{message}</Notice>}
    <section className="section-block" id="courses"><div className="section-heading"><div><span className="eyebrow">YOUR LIBRARY</span><h2>Pick up where you left off</h2></div><span className="count-pill">{courses.length} {courses.length === 1 ? 'course' : 'courses'}</span></div>
      {loading ? <LoadingState label="Loading your courses…" /> : courses.length ? <div className="course-grid">{courses.map((course, index) => <CourseCard key={course.id} course={course} index={index} onDelete={(item) => void remove(item)} />)}</div> : <EmptyState title="Your library starts here">Upload a course PDF and ExamPilot will turn it into a structured knowledge map.</EmptyState>}
    </section>
    <section className="upload-panel"><div className="upload-intro"><span className="upload-icon"><UploadCloud size={22} /></span><div><span className="eyebrow">ADD SOMETHING NEW</span><h2>Bring your course materials</h2><p>Upload text-based or scanned PDFs. We’ll organize concepts so you can focus on learning.</p></div></div>
      <form onSubmit={(event) => void upload(event)} className="upload-form"><label className="field-label" htmlFor="course-title">Course name <span>OPTIONAL</span></label><input id="course-title" className="text-input" value={title} onChange={(event) => setTitle(event.target.value)} placeholder="e.g. Introduction to Biology" maxLength={160} />
        <label className="drop-zone" htmlFor="course-files"><UploadCloud size={23} /><strong>{files.length ? `${files.length} PDF${files.length === 1 ? '' : 's'} selected` : 'Choose course PDFs'}</strong><span>PDF files · multiple files supported</span><input id="course-files" type="file" accept="application/pdf,.pdf" multiple onChange={(event) => setFiles(Array.from(event.target.files ?? []))} /></label>
        {files.length > 0 && <ul className="selected-files" aria-label="Selected files">{files.map((file) => <li key={`${file.name}-${file.size}`}>{file.name}</li>)}</ul>}
        <button className="button button-primary upload-submit" disabled={busy || !files.length}>{busy ? <><LoaderCircle size={17} className="spin" /> Analyzing materials…</> : <><Plus size={17} /> Create learning space</>}</button>
      </form>
    </section><footer className="page-footer">Built for curious minds <span>·</span> Understand · Test · Improve</footer>
  </>;
}
function Stat({ icon, label, value, tone }: { icon: React.ReactNode; label: string; value: number; tone: string }) { return <div className="stat-card"><span className={`stat-icon ${tone}`}>{icon}</span><div><span className="stat-value">{value}</span><span className="stat-label">{label}</span></div></div>; }
function BookOpenIcon() { return <Sparkles size={18} />; }
