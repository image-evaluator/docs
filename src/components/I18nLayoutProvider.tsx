'use client';

import { I18nProvider } from 'fumadocs-ui/i18n';
import { usePathname, useRouter } from 'next/navigation';
import type { ReactNode } from 'react';

export function I18nLayoutProvider({
  locale,
  children,
}: {
  locale: string;
  children: ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();

  const handleLocaleChange = (targetLocale: string) => {
    const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';
    let cleanPath = pathname;

    if (basePath && cleanPath.startsWith(basePath)) {
      cleanPath = cleanPath.slice(basePath.length);
    }

    // Filter out any existing language prefixes ('zh' or 'en')
    const segments = cleanPath.split('/').filter((s) => s.length > 0 && s !== 'zh' && s !== 'en');

    if (targetLocale === 'zh') {
      segments.unshift('zh');
    }

    const nextPath = segments.length > 0 ? `/${segments.join('/')}` : '/';
    router.push(nextPath);
  };

  return (
    <I18nProvider
      locale={locale}
      locales={[
        { locale: 'en', name: 'English' },
        { locale: 'zh', name: '简体中文' },
      ]}
      onLocaleChange={handleLocaleChange}
    >
      {children}
    </I18nProvider>
  );
}

