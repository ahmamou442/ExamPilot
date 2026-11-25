import { useCallback, useEffect, useState } from 'react';
import { coursesApi } from '../api';
import type { Course, Dashboard } from '../types';

export function useCourses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const refresh = useCallback(async () => {
    setLoading(true); setError('');
    try { const [items, stats] = await Promise.all([coursesApi.list(), coursesApi.dashboard().catch(() => null)]); setCourses(items); setDashboard(stats); }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'Unable to load courses.'); }
    finally { setLoading(false); }
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);
  return { courses, dashboard, loading, error, setError, refresh };
}
