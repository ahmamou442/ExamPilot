import { ArrowRight, BookOpen, Clock3, FileText, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { Course } from '../types';

export function CourseCard({ course, index, onDelete }: { course: Course; index: number; onDelete: (course: Course) => void }) {
  return <Link to={`/courses/${course.id}`} className={`course-card card-accent-${index % 4}`}>
    <div className="course-card-top"><span className="course-icon"><FileText size={20} /></span><button type="button" className="icon-button" aria-label={`Delete ${course.title}`} onClick={(event) => { event.preventDefault(); event.stopPropagation(); onDelete(course); }}><Trash2 size={16} /></button></div>
    <span className={`status-tag ${course.status === 'ready' ? 'status-ready' : 'status-pending'}`}><i />{course.status === 'ready' ? 'Ready to learn' : course.status}</span>
    <h3>{course.title}</h3><p>{course.description || 'Your learning workspace is ready when you are.'}</p>
    <div className="card-footer"><span><Clock3 size={14} /> Open course</span><ArrowRight size={17} /></div>
  </Link>;
}
export function CourseEmptyIcon() { return <span className="empty-icon"><BookOpen size={23} /></span>; }
