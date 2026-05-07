// Lesson 01-01: First Green Test
// Generated starter file. Fill in the function bodies.
export function normalizeText(text) {
  // Convert to lowercase.
  text = text.toLowerCase();
  // Trim spaces at the start and end.
  text = text.trim();
  // Collapse internal repeated spaces to one space.
  text = text.replace(/\s+/g, ' ');
  return text;
}


// Lesson 01-02: Counting What the Model Sees
// Generated starter file. Fill in the function bodies.
export function countChars(text) {
  // Return an object mapping each character to count.
    const charCount = {};
    for (const char of text) {
        if (charCount[char]) {
            charCount[char]++;
        } else {
            charCount[char] = 1;
        }
    }
    return charCount;
}

// Lesson 01-03: Random Choice for Generation
// Generated starter file. Fill in the function bodies.
export function weightedRandom(items, weights, rng = Math.random) {
  // Validate equal lengths and non-empty arrays. Treat weights as non-negative. Use cumulative sums and one random draw.
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);
    const cumulativeWeights = [];
    let cumulativeSum = 0;
    for (const w of weights) {
        cumulativeSum += w;
        cumulativeWeights.push(cumulativeSum);
    }
    const randomValue = rng() * totalWeight;
    for (let i = 0; i < cumulativeWeights.length; i++) {
        if (randomValue < cumulativeWeights[i]) {
            return items[i];
        }
    }
}


// Lesson 01-04: Unigram Baseline Generator
// Generated starter file. Fill in the function bodies.
export function trainUnigram(text) {
  // Count characters and convert counts to probabilities.
  // return { items: [], probs: [] };
    const charCount = countChars(text);
    const items = Object.keys(charCount);
    const counts = Object.values(charCount);
    const totalCount = counts.reduce((sum, c) => sum + c, 0);
    const probs = counts.map(c => c / totalCount);
    return { items, probs };
}

export function generateUnigram(model, steps, rng = Math.random) {
  const { items, probs } = model;
  let result = '';
  for (let i = 0; i < steps; i++) {
    result += weightedRandom(items, probs, rng);
  }
  return result;
}


// Lesson 02-01: Tokenize and Vocabulary
// Generated starter file. Fill in the function bodies.
export function buildVocab(text) {
  // Return an object mapping each unique character to a unique integer ID.
  // return { tokenToId: new Map(), idToToken: [] };
    const tokenToId = new Map();
    const idToToken = [];
    let id = 0;
    for (const char of text) {
        if (!tokenToId.has(char)) {
            tokenToId.set(char, id);
            idToToken.push(char);
            id++;
        }
    }
    return { tokenToId, idToToken };
}

export function encode(text, tokenToId) {
    // Convert each character in text to its corresponding ID using tokenToId.
    const ids = [];
    for (const char of text) {
        ids.push(tokenToId.get(char));
    }
    return ids;
}

export function decode(ids, idToToken) {
    // Convert each ID in ids back to its corresponding character using idToToken and concatenate them into a string.
    // Throw clear errors for unknown IDs.
    let text = '';
    for (const id of ids) {
        if (id < 0 || id >= idToToken.length) {
            throw new Error(`Unknown ID: ${id}`);
        }
        text += idToToken[id];
    }
    return text;
}


// Lesson 02-02: Build Bigram Counts
// Generated starter file. Fill in the function bodies.
export function buildBigramCounts(ids, vocabSize) {
  // Return a 2D array bigramCounts where bigramCounts[i][j] counts how many times token ID j follows token ID i in the sequence of ids.
    const bigramCounts = Array.from({ length: vocabSize }, () => Array(vocabSize).fill(0));
    for (let i = 0; i < ids.length - 1; i++) {
        const currentId = ids[i];
        const nextId = ids[i + 1];
        bigramCounts[currentId][nextId]++;
    }
    return bigramCounts;
}


// Lesson 02-03: Bigram Probabilities and Predict
// Generated starter file. Fill in the function bodies.
export function bigramProbs(counts) {
    // Convert bigramCounts to bigramProbs by normalizing each row to sum to 1. Handle rows that sum to zero by assigning a uniform distribution over the vocabulary.
    const bigramProbs = counts.map(row => {
        const rowSum = row.reduce((sum, count) => sum + count, 0);
        if (rowSum === 0) {
            // If no counts, assign uniform probabilities
            return Array(row.length).fill(1 / row.length);
        }
        return row.map(count => count / rowSum);
    });
    return bigramProbs;
}

export function predictNext(currentId, probs, rng = Math.random) {
  // Given the current token ID and the bigramProbs matrix, return the next token ID by sampling from the probability distribution in the row corresponding to currentId.
  return weightedRandom([...Array(probs[currentId].length).keys()], probs[currentId], rng);
}
