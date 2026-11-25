import type { ReactNode } from 'react';
import { BookOpen, GraduationCap, LayoutDashboard, Sparkles } from 'lucide-react';
import { Link, NavLink } from 'react-router-dom';

export function AppLayout({ children }: { children: ReactNode }) {
  return <div className="app-shell">
    <a className="skip-link" href="#main-content">Skip to content</a>
    <aside className="sidebar">
      <Link to="/" className="brand" aria-label="ExamPilot home"><span className="brand-mark"><GraduationCap size={21} /></span><span>ExamPilot<small>YOUR LEARNING STUDIO</small></span></Link>
      <div className="nav-label">WORKSPACE</div>
      <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}><LayoutDashboard size={18} /> Overview</NavLink>
      <a className="nav-link" href="/#courses"><BookOpen size={18} /> My courses</a>
      <div className="sidebar-note"><Sparkles size={17} /><p>Small steps add up.<br /><strong>Keep your momentum.</strong></p></div>
      <div className="sidebar-bottom">Learn with intention<span>Understand · Test · Improve</span></div>
    </aside>
    <main className="main-area" id="main-content"><header className="topbar"><span className="topbar-label">PERSONAL LEARNING SPACE</span><span className="online"><i /> All systems ready</span></header><div className="page-content">{children}</div></main>
  </div>;
}
