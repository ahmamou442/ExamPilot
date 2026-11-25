import { Navigate, Route, Routes } from 'react-router-dom';
import { AppLayout } from './components/AppLayout';
import { HomePage } from './pages/HomePage';
import { CoursePage } from './pages/CoursePage';
import { QuizPage } from './pages/QuizPage';
import { LearnPage } from './pages/LearnPage';

export default function App() {
  return <AppLayout><Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/courses/:id" element={<CoursePage />} />
    <Route path="/diagnostic/:id" element={<QuizPage kind="diagnostic" />} />
    <Route path="/exam/:id" element={<QuizPage kind="exam" />} />
    <Route path="/learn/:id/:concept" element={<LearnPage />} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes></AppLayout>;
}
