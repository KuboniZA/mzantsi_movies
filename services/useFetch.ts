import { useCallback, useEffect, useRef, useState } from "react";

const useFetch = <T>(fetchFunction: () => Promise<T>, autoFetch = true) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const isMounted = useRef<boolean>(true);

  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchFunction();

      if (isMounted.current) {
        setData(result);
      }
    } catch (err) {
      if (isMounted.current) {
        setError(
          err instanceof Error
            ? err
            : new Error("An error occurred while fetching data."),
        );
      }
    } finally {
      if (isMounted.current) {
        setLoading(false);
      }
    }
  }, [fetchFunction]);

  const reset = useCallback(() => {
    if (isMounted.current) {
      setData(null);
      setLoading(false);
      setError(null);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchData();
    }
  }, [autoFetch, fetchData]);

  return { data, loading, error, refetch: fetchData, reset };
};

export default useFetch;
