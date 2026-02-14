import React, { useState } from "react";
import Header from "./components/Header";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";

function App() {

  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen p-10">
      <Header />
      <InputForm setResult={setResult} />
      <ResultCard result={result} />
    </div>
  );
}

export default App;
