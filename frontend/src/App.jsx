import React from 'react';
import AskQuery from './components/AskQuery';
import CropClassifier from './components/CropClassifier';

function App() {
    return (
        <div className="App">
            <header className="bg-gray-800 p-4">
                <nav className="flex justify-between items-center">
                    <h1 className="text-white text-3xl">CropCare AI</h1>
                    <ul className="flex space-x-4">
                        <li><a href="#ask-query" className="text-white hover:underline">Ask Query</a></li>
                        <li><a href="#crop-classifier" className="text-white hover:underline">Crop Classifier</a></li>
                    </ul>
                </nav>
            </header>
            <main className="p-4">
                <AskQuery />
                <CropClassifier />
            </main>
            <footer className="bg-gray-800 p-4 text-white text-center">
                <p>Created by Swayam</p>
            </footer>
        </div>
    );
}

export default App;
