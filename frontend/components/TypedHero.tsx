'use client';

import { useEffect, useRef } from 'react';

const SF_DISPLAY = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif";

export default function TypedHero() {
  const elRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    let typed: import('typed.js').default | null = null;

    import('typed.js').then(({ default: Typed }) => {
      if (!elRef.current) return;
      typed = new Typed(elRef.current, {
        strings: [
          'Predict game outcomes.',
          '6 ML models. Real NBA data.',
          'Find the winning edge.',
        ],
        typeSpeed: 40,
        backSpeed: 22,
        backDelay: 2400,
        loop: true,
        showCursor: true,
        cursorChar: '|',
      });
    });

    return () => {
      typed?.destroy();
    };
  }, []);

  return (
    <p
      style={{
        fontFamily: SF_DISPLAY,
        fontSize: '15px',
        fontWeight: 600,
        color: 'rgba(255,255,255,0.5)',
        letterSpacing: '0.2px',
        minHeight: '1.5em',
        marginBottom: '20px',
      }}
    >
      <span ref={elRef} />
    </p>
  );
}
