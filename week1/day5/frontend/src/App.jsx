import { useState } from "react";
import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      setResume(null);
      return;
    }

    const validFile =
      file.name.toLowerCase().endsWith(".pdf") ||
      file.name.toLowerCase().endsWith(".docx");

    if (!validFile) {
      setError("Only PDF and DOCX files are supported.");
      setResume(null);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Resume file must be smaller than 10 MB.");
      setResume(null);
      return;
    }

    setError("");
    setResume(file);
  };

  const handleAnalyze = async () => {
    setError("");
    setResult(null);

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    if (!resume) {
      setError("Please upload your resume.");
      return;
    }

    const formData = new FormData();

    formData.append("job_description", jobDescription);
    formData.append("resume", resume);

    try {
      setLoading(true);

      const response = await fetch(
        `${API_URL}/api/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume analysis failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const score =
    result?.analysis?.overall_match_percentage ?? 0;

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">
        <div className="brand">

          <div className="logo">
            AI
          </div>

          <div>
            <h1>
              Resume Intelligence
            </h1>

            <p>
              AI-Powered Resume Evaluation
            </p>
          </div>

        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Engine Ready
        </div>
      </header>


      {/* MAIN */}

      <main className="container">

        {/* HERO */}

        <section className="hero">

          <span className="badge">
            AI RESUME ANALYZER
          </span>

          <h2>
            Find out how well your resume
            matches a job.
          </h2>

          <p>
            Upload your resume, paste the job
            description, and let AI analyze your
            skills, experience and job fit.
          </p>

        </section>


        {/* INPUTS */}

        <section className="input-grid">

          {/* JOB DESCRIPTION */}

          <div className="card">

            <div className="card-header">

              <div>
                <h3>
                  Job Description
                </h3>

                <p>
                  Paste the complete job description
                </p>
              </div>

              <span className="step">
                01
              </span>

            </div>

            <textarea
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(
                  event.target.value
                )
              }
              placeholder="Paste the job description here..."
            />

            <div className="character-count">
              {jobDescription.length} characters
            </div>

          </div>


          {/* RESUME */}

          <div className="card">

            <div className="card-header">

              <div>
                <h3>
                  Resume
                </h3>

                <p>
                  Upload your latest resume
                </p>
              </div>

              <span className="step">
                02
              </span>

            </div>

            <label className="upload-area">

              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
              />

              <div className="upload-icon">
                ↑
              </div>

              <strong>
                {resume
                  ? resume.name
                  : "Upload Resume"}
              </strong>

              <span>
                {resume
                  ? `${(
                      resume.size / 1024
                    ).toFixed(1)} KB`
                  : "PDF or DOCX • Max 10 MB"}
              </span>

            </label>

          </div>

        </section>


        {/* ERROR */}

        {error && (
          <div className="error">
            {error}
          </div>
        )}


        {/* ANALYZE BUTTON */}

        <button
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing Resume..."
            : "Analyze Resume →"}
        </button>


        {/* LOADING */}

        {loading && (
          <div className="loading-card">

            <div className="spinner"></div>

            <h3>
              AI is analyzing your resume
            </h3>

            <p>
              Extracting resume information,
              analyzing the job description,
              and calculating the match score.
            </p>

          </div>
        )}


        {/* RESULTS */}

        {result && !loading && (

          <section className="results">

            <div className="results-title">

              <div>

                <span className="badge">
                  ANALYSIS COMPLETE
                </span>

                <h2>
                  Resume Analysis
                </h2>

              </div>

              <div className="score-circle">

                <strong>
                  {Math.round(score)}
                </strong>

                <span>
                  %
                </span>

              </div>

            </div>


            {/* CANDIDATE + VERDICT */}

            <div className="result-grid">

              <div className="result-card">

                <h3>
                  Candidate
                </h3>

                <h4>
                  {result.candidate.name ||
                    "Candidate"}
                </h4>

                {result.candidate.email && (
                  <p>
                    {result.candidate.email}
                  </p>
                )}

                {result.candidate.phone && (
                  <p>
                    {result.candidate.phone}
                  </p>
                )}

                <p>
                  Experience:{" "}
                  {
                    result.candidate
                      .experience_years
                  }{" "}
                  years
                </p>

              </div>


              <div className="result-card">

                <h3>
                  Match Verdict
                </h3>

                <div className="verdict">
                  {
                    result.analysis
                      .final_verdict
                  }
                </div>

                <p>
                  Experience requirement:{" "}
                  <strong>
                    {
                      result.analysis
                        .experience_requirement_met
                        ? "Met"
                        : "Not Met"
                    }
                  </strong>
                </p>

              </div>

            </div>


            {/* MATCHING SKILLS */}

            <div className="result-card">

              <h3>
                Matching Skills
              </h3>

              <div className="tags">

                {result.analysis.matching_skills
                  .length > 0 ? (

                  result.analysis
                    .matching_skills
                    .map((skill, index) => (
                      <span
                        className="tag match"
                        key={index}
                      >
                        {skill}
                      </span>
                    ))

                ) : (

                  <span>
                    No matching skills found.
                  </span>

                )}

              </div>

            </div>


            {/* MISSING SKILLS */}

            <div className="result-card">

              <h3>
                Missing Important Skills
              </h3>

              <div className="tags">

                {result.analysis
                  .missing_important_skills
                  .length > 0 ? (

                  result.analysis
                    .missing_important_skills
                    .map((skill, index) => (
                      <span
                        className="tag missing"
                        key={index}
                      >
                        {skill}
                      </span>
                    ))

                ) : (

                  <span>
                    No important missing skills.
                  </span>

                )}

              </div>

            </div>


            {/* RESUME SKILLS */}

            <div className="result-card">

              <h3>
                Resume Skills
              </h3>

              <div className="tags">

                {result.candidate.skills.map(
                  (skill, index) => (
                    <span
                      className="tag"
                      key={index}
                    >
                      {skill}
                    </span>
                  )
                )}

              </div>

            </div>


            {/* PROJECTS */}

            <div className="result-card">

              <h3>
                Projects
              </h3>

              {result.candidate.projects.length > 0 ? (

                result.candidate.projects.map(
                  (project, index) => (
                    <div
                      className="list-item"
                      key={index}
                    >
                      {project}
                    </div>
                  )
                )

              ) : (

                <p>
                  No projects found.
                </p>

              )}

            </div>


            {/* EDUCATION */}

            <div className="result-card">

              <h3>
                Education
              </h3>

              {result.candidate.education.length > 0 ? (

                result.candidate.education.map(
                  (education, index) => (

                    <div
                      className="education-item"
                      key={index}
                    >

                      <strong>
                        {education.degree}
                      </strong>

                      <span>
                        {education.institution}
                      </span>

                      <span>
                        {education.year}
                      </span>

                    </div>

                  )
                )

              ) : (

                <p>
                  No education information found.
                </p>

              )}

            </div>

          </section>
        )}

      </main>


      <footer>
        AI Resume Intelligence Platform
        <span> • </span>
        FastAPI + Groq + React
      </footer>

    </div>
  );
}

export default App;