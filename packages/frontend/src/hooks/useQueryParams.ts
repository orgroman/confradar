import { useSearchParams } from 'react-router-dom';
import { useCallback } from 'react';

/**
 * Custom hook for managing URL query parameters
 * Useful for filter state that should persist in the URL
 */
export function useQueryParams<T extends Record<string, string>>() {
  const [searchParams, setSearchParams] = useSearchParams();

  const getParam = useCallback(
    (key: keyof T): string | null => {
      return searchParams.get(key as string);
    },
    [searchParams]
  );

  const setParam = useCallback(
    (key: keyof T, value: string | null) => {
      const newParams = new URLSearchParams(searchParams);
      if (value === null || value === '') {
        newParams.delete(key as string);
      } else {
        newParams.set(key as string, value);
      }
      setSearchParams(newParams);
    },
    [searchParams, setSearchParams]
  );

  const setParams = useCallback(
    (params: Partial<T>) => {
      const newParams = new URLSearchParams(searchParams);
      Object.entries(params).forEach(([key, value]) => {
        if (value === null || value === '') {
          newParams.delete(key);
        } else {
          newParams.set(key, value as string);
        }
      });
      setSearchParams(newParams);
    },
    [searchParams, setSearchParams]
  );

  const clearParams = useCallback(() => {
    setSearchParams(new URLSearchParams());
  }, [setSearchParams]);

  const getAllParams = useCallback((): Partial<T> => {
    const params: any = {};
    searchParams.forEach((value, key) => {
      params[key] = value;
    });
    return params;
  }, [searchParams]);

  return {
    getParam,
    setParam,
    setParams,
    clearParams,
    getAllParams,
  };
}
