% *----------------------------------------------------------------------
% *
% * iisthesis.cls - PWr/IZ/IIS thesis LaTeX template
% * Copyright (C) 2006  Michal Stanek
% *
% * The template was adapted to be compliance with the newest editorial
% * requirements introduced on the IIS/PWr department in the May 2006.
% *
% * modified skz_thesis.sty created by Michal Stochmialek
% * modified from University of Tulsa MS Thesis class
% * modified from the University of Washington thesis class
% *
% *----------------------------------------------------------------------
% *	LICENCE
% *
% * This library is free software; you can redistribute it and/or
% * modify it under the terms of the GNU Lesser General Public
% * License as published by the Free Software Foundation; either
% * version 2.1 of the License, or (at your option) any later version.
% *
% * This library is distributed in the hope that it will be useful,
% * but WITHOUT ANY WARRANTY; without even the implied warranty of
% * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
% * Lesser General Public License for more details.
% *
% * You should have received a copy of the GNU Lesser General Public
% * License along with this library; if not, write to the Free Software
% * Foundation, Inc., 59 Temple Place, Suite 330, Boston,
% * MA  02111-1307  USA
% *----------------------------------------------------------------------
% *

\ProvidesClass{iisthesis}[2006/05/21]
\NeedsTeXFormat{LaTeX2e}


%
% ----  Thesis is a modified 12-pt mwbk style  ----------------------------
%

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{mwbk}}
\newif\if@color
\DeclareOption{color}{\@colortrue}
\PassOptionsToClass{12pt}{mwbk}
\PassOptionsToClass{a4paper}{mwbk}
\PassOptionsToClass{openright}{mwbk}
\ProcessOptions
\LoadClass{mwbk}

%% miejsce na szycie
\if@twoside
	\usepackage[a4paper, left=2.5cm, right=2.5cm, top=3.5cm, bottom=2.5cm, headsep=0.6cm, bindingoffset=0.5cm]{geometry}
%	\usepackage[a4paper, left=3cm, right=3cm, top=3cm, bottom=3cm, headsep=0.6cm, bindingoffset=0.5cm]{geometry}
\else
	\usepackage[a4paper, left=3.0cm, right=2.5cm, top=3.5cm, bottom=2.5cm, headsep=0.6cm, ]{geometry}
\fi

\RequirePackage{ifpdf}

% komenda ifpdf
%\newif\ifpdf
%\ifx\pdfoutput\undefined
        %\pdffalse
%\else
        %\pdfoutput=1
        %\pdftrue
%\fi

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[english]{babel}

%\usepackage[polish]{babel}
%\usepackage[polish, english]{babel}
%\usepackage[cp1250]{inputenc}
\usepackage{colortbl}
\usepackage{multirow}
%\usepackage{theorem}

%\usepackage[small,normal,bf,up]{caption}

%\usepackage[Lenny]{sty/fncychap}

% obrazki
\ifpdf
  \usepackage[pdftex]{graphicx}
  \DeclareGraphicsExtensions{.pdf,.png}
\else
  \usepackage[dvips]{graphicx}
  \DeclareGraphicsExtensions{.eps,.ps, .png}
\fi

%\linespread{1.5}

% Rysunek 1: => Rys. 1.
%\addto\captionspolish{
   %\def\figurename{Rys.}%
   %\def\algorithmname{Algorytm}%
   %\def\tablename{\textbf{Tabela}}%
%}
\def\captionlabel#1{\textbf{#1.} }
\renewcommand \thefigure {\thechapter.\@arabic\c@figure}

%
% Bardziej wyraziste wypunktowania
%
%\renewcommand{\labelitemi}{$\bullet$}
%\renewcommand{\labelitemii}{$\circ$}

%
% Delikatniejsze wypunktowania
%
\renewcommand{\labelitemi}{$\circ$}
\renewcommand{\labelitemii}{$\cdot$}

% Odstï¿½p wypunktowania od tekstu
\addtolength{\leftmargini}{3mm}

% kombinacje z naglowkami/stopkami
\usepackage{fancyhdr}

%\fancypagestyle{headings}{
%\setlength\headheight{14.5pt}
%   \fancyhf{}
%   \renewcommand\headrulewidth{0.4pt}
%
%	 %\renewcommand\footrulewidth{0.2pt}
%   \if@twoside
%   	\fancyhead[LO]{\emph{\nouppercase{\leftmark}}}
%   	\fancyhead[RE]{\emph{\@title}}
%   	\fancyhead[LE, RO]{\thepage}
%   \else
%   	\fancyhead[L]{\emph{\nouppercase{\leftmark}}}
%    \fancyhead[R]{\thepage}
%   \fi
%}

  \if@twoside
		\renewcommand\hf@headings{%
		\def\@oddhead{\vtop{%
		      \hb@xt@\textwidth{%
		        %\reset@font{\heading@font\rightmark}\hfil\thepage\strut}
		        \reset@font{\heading@font{\leftmark}}\hfil\strut\footnotesize\thepage}
		      \vskip1pt\hrule height 0.4pt \vskip-2.4pt}}%
		  \let\@oddfoot\@empty

		  \def\@evenhead{\vtop{%
		      \hb@xt@\textwidth{%
		        %\reset@font\strut\thepage\hfil\heading@font\leftmark}%
		        \reset@font{\footnotesize\strut\thepage\hfil\heading@font\@title}}
		        \vskip2pt\hrule \vskip-2.4pt}}%
		  \let\@evenfoot\@empty
		}
   \else
   \renewcommand\hf@headings{%
   		\def\@oddhead{\vtop{%
		      \hb@xt@\textwidth{%
   			\reset@font{\heading@font\rightmark}\hfil\thepage}%
   			\vskip1pt\hrule height 0.4pt \vskip-2.4pt}}%
		  \def\@evenhead{\reset@font\thepage\hfil\heading@font\leftmark}%

		  \let\@oddfoot\@empty
		  \let\@evenfoot\@empty
%		  \def\@oddfoot{\vtop{%
%		      \hb@xt@\textwidth{%
% 							\hfil}
%   			\vskip10pt\hrule height 0.4pt \vskip10.4pt}}%
%
%		  \def\@evenfoot{\hrule}
		  }
   \fi


\fancypagestyle{opening}{
\setlength\headheight{14.5pt}
   \fancyhf{}
   \renewcommand\headrulewidth{0.4pt}

	 %\renewcommand\footrulewidth{0.2pt}
   \if@twoside
   	\fancyhead[LO]{\emph{\nouppercase{\leftmark}}}
   	\fancyhead[RE]{\emph{\@title}}
   	\fancyhead[LE, RO]{\thepage}
   \else
   	\fancyhead[L]{\emph{\nouppercase{\leftmark}}}
    \fancyhead[R]{\thepage}
   \fi
}


%\fancypagestyle{empty}{%
%	 \fancyhf{}
%   \renewcommand\headrulewidth{0.4pt}
%   %\renewcommand\footrulewidth{0.2pt}
%   \if@twoside
%   	\fancyhead[LO]{\emph{\nouppercase{\leftmark}}}
%   	\fancyhead[RE]{\emph{\@title}}
%   	\fancyhead[LE, RO]{\thepage}
%   \else
%   	\fancyhead[L]{\emph{\nouppercase{\leftmark}}}
%    \fancyhead[R]{\thepage}
%   \fi
%}

\def\advisor#1{\gdef\@advisor{#1}}
\def\thanks#1{\gdef\@thanks{#1}}
\def\abstractPL#1{\gdef\@abstractPL{#1}}
\def\abstractSH#1{\gdef\@abstractSH{#1}}
\def\abstractEN#1{\gdef\@abstractEN{#1}}

\def\slowaKluczowe#1{\gdef\@slowaKluczowe{#1}}
\def\instituteLogo#1{\gdef\@instituteLogo{#1}}

\instituteLogo{logos/pwr}

\renewcommand\maketitle {
   \pagenumbering{arabic}
   \thispagestyle{empty}

   \noindent
   %\includegraphics[width=\textwidth]{\@instituteLogo}
\begin{flushleft}
\includegraphics[width=9.32cm]{\@instituteLogo}
\begin{tabular*}{\textwidth}{>{\columncolor[gray]{.8}}p{0.57cm}>{\columncolor[gray]{.8}}p{0.57cm}|p{13.5cm}}
	\hline
	 & &\large{\bfseries{\rule{0pt}{0.5cm}\ Faculty of Computer Science and Management}} \\[3pt]
	 & &\ \ \large{degree course: Computer Science}\\
	 & &\ \ speciality: Fundamental Problems of Computer Science\\
	 & &\multicolumn{1}{c}{\rule{0pt}{2.5cm} \Large{Master's Thesis}} \\
	 & &\multicolumn{1}{p{13.5cm}}{\rule{0pt}{2cm}\centering\bfseries\sc\Large{\@title}} \\
	 & &\multicolumn{1}{c}{\rule{0pt}{1.5cm}\large\@author} \\
	 & &\multicolumn{1}{p{13.5cm}}{\rule{0pt}{2cm}\small\begin{flushright}\noindent keywords:\\ \@slowaKluczowe\end{flushright}} \\
	 & & \multicolumn{1}{p{13.5cm}}{
		\begin{flushright}
					\begin{tabular}{p{13.0cm}}
							 \small short abstract:\newline \@abstractSH
					\end{tabular}
		\end{flushright}
%	 	\rule{0.5cm}{1cm}{\small krï¿½tkie streszczenie:\newline \@abstractSH}
	 	} \\
	 	& & \multicolumn{1}{p{13.5cm}}{
		\begin{center}
					\begin{tabular}{|c|c|c|c|}
							 \hline
							 \multirow{2}{*}{\small{Supervisor:}} & \multirow{2}{*}{\small{dr inż. Krzysztof Juszczyszyn}} & \scriptsize{ } & \scriptsize{ } \\
							  &  & \small{......................} & \small{.......................} \\
							 \hline
							 \ & \scriptsize\textit{name and surname} & \scriptsize\textit{grade} & \scriptsize\textit{signature} \\
							 \hline
					\end{tabular}
		\end{center}
		} \\
	& & \rule{0pt}{0.7cm} \\
	&\multicolumn{1}{>{\columncolor[gray]{0.0}}p{0.57cm}|}{} & \multicolumn{1}{c}{\rule{0pt}{0.7cm} \large{Wrocław \@date}}

\end{tabular*}
\end{flushleft}

% \begin{center}
%			 \vspace{3cm} {\sf\large Praca Magisterska} \\
%      \vspace{.5cm} {\sf\Huge \@title}  \\
%      \vspace{1cm} {\sf\Large \@author} \\
%      \vspace{6cm}
%      \begin{tabular}{@{}l@{}}
%          \large {\bf Promotor:} \@advisor \\\\
%          \large {\bf Ocena:}
%     \end{tabular}
%
%      \vspace{4cm} \large Wroc\l aw \@date
%   \end{center}
% \if@twoside
%    \clearpage
%
%
% 	 \pagestyle{plain}
% 	 ~ \vspace{\textheight} \\
% 	 ~ \vspace{13cm} \\
%    %
%
% 	 {
%
% 	 		\begin{flushright}
% 					\begin{tabular}{p{9.3cm}}
% 							Składam serdeczne podziękowania Promotorowi, Panu \@advisor za okazaną życzliwość, zrozumienie, pomoc oraz cenne uwagi przekazywane w trakcie przygotowywania niniejszej pracy.
%
% 							\\
% 							\\
%
% 							\@thanks
% 					\end{tabular}
% 			\end{flushright}
%
%
%
% 			\begin{center}\small Niniejszy dokument zosta\l\ z\l o\.zony w systemie \LaTeX.\end{center}
% 	 }
%
%    ~ \vspace{-3cm} \\
%    ~ \vspace{\textheight} \\
%    %{\begin{center}\small Niniejszy dokument zosta\l\ z\l o\.zony w systemie \LaTeX.\end{center}}
% \else
% 	 \pagestyle{plain}
% \fi



   %\selectlanguage{polish}
   \tableofcontents


   \clearpage
	 \pagestyle{plain}
   \begin{center}
   \begin{tabular}{@{}l@{}c@{}}
      \begin{minipage}{\textwidth}
         \begin{abstract}
            \noindent
            \@abstractEN
         \end{abstract}

         \vspace{1.5cm}

         \selectlanguage{polish}
         \begin{abstract}
            \noindent
            \@abstractPL
         \end{abstract}
         \selectlanguage{english}
      \end{minipage}
   &
      \begin{tabular}{@{}l@{}}\rule{0pt}{0.9\textheight}\end{tabular}
   \end{tabular}
   \end{center}

   \if@twoside
   	\cleardoublepage
   \else
   	\clearpage
   \fi
   \pagestyle{headings}
}

\newenvironment{abstract}
   {\small
     \begin{center}%
       {\bfseries \abstractname\vspace{-.5em}\vspace{\z@}}%
     \end{center}%
     \quotation}
   {\endquotation}

\newif\if@textpages
\def\textpages{% Start of text pages
   \clearpage\pagestyle{plain}
   \cleardoublepage\pagestyle{headings}
   %\pagenumbering{arabic}
   %\setcounter{page}{1}
   \@textpagestrue

   % info o pracy do pdfa
   \ifpdf
     \pdfinfo {
        /Author (\@author)
        /Title (\@title)
        /Subject (Praca Magisterska)
     }
   \fi
  }


% redefinicja komendy z mwbk (dodane phantomsection) -> hyperref dziala
\renewcommand*\chapter@toc{%
  \ifHeadingNumbered\typeout{\@chapapp\space\thechapter.}\fi
  \ifpdf \phantomsection \fi
  \if@textpages
    \addcontentsline{toc}{chapter}{%
        \ifHeadingNumbered
      \mw@seccntformat{\@chapapp\ \HeadingNumber}%
        \fi
        \HeadingTOCText}%
    \addtocontents{lof}{\protect\addvspace{10\p@}}%
    \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \fi
  }

\SetSectionFormatting[breakbefore,wholewidth]{chapter}
        {0\p@}
        {\FormatRigidChapterHeading{11\baselineskip}{12\p@}%
           {\Large\@chapapp\space}{\Huge}}
        {3\baselineskip}


% linki (backref = lista odwolan, bookmarksopen = rozwiniete bookmarki)
\ifpdf
  \if@color
    \usepackage[bookmarks=true, bookmarksnumbered, pdfview=FitH, breaklinks, colorlinks, citecolor=blue, pdfpagelabels, pdftex]{hyperref}
  \else
    \usepackage[plainpages=false, bookmarks=true, bookmarksnumbered, pdfstartview=FitH, breaklinks, colorlinks=false, pdfborder=0 0 0, pdftex]{hyperref}
  \fi

  % wylacza ostrzezenia dotyczace bookmarkow pdfa
  \pdfstringdefDisableCommands{\def\enspace{ }}
\else
  % using hyperref in PostScript gives url command with correct line breaks
  \usepackage[hypertex]{hyperref}
\fi

% lepsze formatowanie przypisow dolnych
\newlength{\fnBreite}\settowidth{\fnBreite}{\footnotesize 00.i}%
\renewcommand{\@makefntext}[1]{%
  \protect\footnotesize\upshape%
  \setlength{\@tempdima}{\columnwidth}\addtolength{\@tempdima}{-\fnBreite}%
  \makebox[\fnBreite][r]{\@thefnmark.\phantom{i}}%
  \parbox[t]{\@tempdima}{\everypar{\hspace*{1em}}\hspace*{-1em}\upshape#1}}


\let\oldthebibliography=\thebibliography
\let\endoldthebibliography=\endthebibliography
\renewenvironment{thebibliography}[1]{%
  \begin{oldthebibliography}{#1}%
    \setlength{\parskip}{0ex}%
    \setlength{\itemsep}{.5\baselineskip}}% space between entries
{\end{oldthebibliography}}

\SetSectionFormatting[runin]{paragraph}
        {5pt plus 2pt minus 2pt}
        {\FormatRunInHeading{\bf}}
        {.5em}
\SetSectionFormatting[runin]{subparagraph}
        {3pt plus 2pt minus 2pt}
        {\FormatRunInHeading{\it}}
        {.5em}



%%%%%%%%%%%%%%%%%%%%%%%%%%
%\theoremstyle{break}
%{
%  \theorembodyfont{\upshape}
%	\theoremheaderfont{\normalsize\bfseries}
%	\newtheorem{definition}{Definicja}[chapter]
%}

