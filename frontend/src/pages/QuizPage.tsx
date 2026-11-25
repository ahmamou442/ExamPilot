import { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, Check, CircleHelp, LoaderCircle, Sparkles } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { assessmentApi } from '../api';
import { LoadingState, Notice } from '../components/States';
import type { Assessment, Question, QuizResult } from '../types';

export function QuizPage({ kind }: { kind: 'diagnostic' | 'exam' }) {
  const { id = '' } = useParams(); const [assessment, setAssessment] = useState<Assessment | null>(null); const [index, setIndex] = useState(0); const [answers, setAnswers] = useState<Record<string, string>>({}); const [result, setResult] = useState<QuizResult | null>(null); const [error, setError] = useState(''); const [busy, setBusy] = useState(false);
  useEffect(() => { let mounted = true; const request = kind === 'diagnostic' ? assessmentApi.getDiagnostic(id) : assessmentApi.getExam(id); request.then((data) => { if (!mounted) return; setAssessment(data); setAnswers(data.answers ?? {}); }).catch((cause: unknown) => { if (mounted) setError(cause instanceof Error ? cause.message : 'Could not load assessment.'); }); return () => { mounted = false; }; }, [id, kind]);
  const questions = assessment?.questions ?? []; const current: Question | undefined = questions[index]; const answeredCount = Object.keys(answers).length;
  async function submitAnswer() {
    if (!current || !answers[current.id]) return; setBusy(true); setError('');
    try {
      if (kind === 'diagnostic') { const response = await assessmentApi.answerDiagnostic(id, current.id, answers[current.id]); if (response.completed && response.results) setResult(response.results); else if (index + 1 < questions.length) setIndex(index + 1); else setError('Answer saved, but results are not ready yet.'); }
      else if (index + 1 < questions.length) setIndex(index + 1);
      else setResult(await assessmentApi.submitExam(id, answers));
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Could not save your answer.'); }
    finally { setBusy(false); }
  }
  const percent = useMemo(() => questions.length ? Math.round((answeredCount / questions.length) * 100) : 0, [answeredCount, questions.length]);
  if (error && !assessment) return <Notice error>{error}</Notice>;
  if (!assessment) return <LoadingState label="Preparing your questions…" />;
  if (!questions.length) return <Notice error>This assessment has no questions.</Notice>;
  return <><Link to="/" className="back-link"><ArrowLeft size={16} /> Leave assessment</Link><section className="quiz-wrap"><div className="quiz-heading"><span className="eyebrow">{kind === 'exam' ? 'PRACTICE MODE' : 'DISCOVER WHAT YOU KNOW'}</span><h1>{result ? 'A little progress goes a long way.' : kind === 'exam' ? 'Practice exam' : 'Knowledge check'}</h1><p>{result ? 'Here’s a snapshot of your understanding so far.' : 'Take your time. This is a chance to learn, not just a score.'}</p></div>
    {result ? <div className="result-card"><span className="result-icon"><Check size={24} /></span><div className="result-score">{result.percentage}<small>%</small></div><p>You got <strong>{result.score} of {result.total}</strong> questions right.</p>{result.details?.map((item, i) => <div className="result-detail" key={item.question_id || i}><span>{item.correct ? '✓' : '↻'}</span>{item.explanation || `Question ${i + 1}`}</div>)}<Link className="button button-primary" to="/">Back to your library <ArrowRight size={16} /></Link></div> : <div className="question-card"><div className="progress-meta"><span>QUESTION {index + 1} <span className="muted">OF {questions.length}</span></span><span>{percent}% complete</span></div><div className="progress-track" role="progressbar" aria-label="Assessment progress" aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}><span style={{ width: `${percent}%` }} /></div><h2>{current?.question}</h2><div className="options-list" role="group" aria-label="Answer options">{Object.entries(current?.options ?? {}).map(([key, value]) => <button key={key} type="button" aria-pressed={answers[current!.id] === key} className={`option-button ${answers[current!.id] === key ? 'selected' : ''}`} onClick={() => setAnswers({ ...answers, [current!.id]: key })}><span className="option-key">{key}</span><span>{value}</span>{answers[current!.id] === key && <Check size={17} />}</button>)}</div>{error && <Notice error>{error}</Notice>}<div className="question-footer"><span><Sparkles size={15} /> One question at a time</span><button className="button button-primary" disabled={!answers[current?.id ?? ''] || busy} onClick={() => void submitAnswer()}>{busy ? <LoaderCircle className="spin" size={17} /> : index + 1 === questions.length ? 'Finish assessment' : 'Save & continue'}{!busy && <ArrowRight size={16} />}</button></div></div>}
  </section></>;
}
