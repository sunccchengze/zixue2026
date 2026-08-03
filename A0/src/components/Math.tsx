import katex from 'katex';
import 'katex/dist/katex.min.css';

interface MathProps {
  tex: string;
  display?: boolean;
  className?: string;
}

export default function MathTex({ tex, display = false, className = '' }: MathProps) {
  const html = katex.renderToString(tex, {
    displayMode: display,
    throwOnError: false,
    trust: true,
  });

  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
