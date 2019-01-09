// http://yann.lecun.com/exdb/mnist/

const MAX_TRAINING_SIZE = 2000;

const fs = require("fs").promises;
const Brain = require("./Brain");

const loadTrainingLabelsData = async () => {
  try {
    let position = 0;

    const labelsFile = await fs.open(
      "./training-data/train-labels-idx1-ubyte",
      "r"
    );
    const buffer = Buffer.alloc(4);
    await labelsFile.read(buffer, 0, 4, position);
    position += 4;
    const magicNumber = buffer.readInt32BE();
    await labelsFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfItems = buffer.readInt32BE();
    const labels = [];
    for (let i = 0; i < numberOfItems && i < MAX_TRAINING_SIZE; i++) {
      await labelsFile.read(buffer, 0, 1, position);
      position += 1;
      const label = buffer.readInt8();
      labels.push(label);
      console.log("\033[2J");
      console.log(`Reading image label ${i + 1} out of ${numberOfItems}`);
    }

    labelsFile.close();

    return labels;
  } catch (e) {
    console.log(e);
  }
};

const loadTrainingImagesData = async () => {
  try {
    let position = 0;

    const imagesFile = await fs.open(
      "./training-data/train-images-idx3-ubyte",
      "r"
    );
    const buffer = Buffer.alloc(4);
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const magicNumber = buffer.readInt32BE();
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfItems = buffer.readInt32BE();
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfRows = buffer.readInt32BE();
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfColumns = buffer.readInt32BE();
    const images = [];
    for (let i = 0; i < numberOfItems && i < MAX_TRAINING_SIZE; i++) {
      const image = [];
      for (let j = 0; j < numberOfRows; j++) {
        for (let k = 0; k < numberOfColumns; k++) {
          await imagesFile.read(buffer, 0, 1, position);
          position += 1;
          const pixel = buffer.readInt8();
          image.push(pixel);
        }
      }
      console.log("\033[2J");
      console.log(`Reading image ${i + 1} out of ${numberOfItems}`);
      images.push(image);
    }

    imagesFile.close();

    return images;
  } catch (e) {
    console.log(e);
  }
};

const loadTestLabelsData = async () => {
  try {
    let position = 0;

    const labelsFile = await fs.open("./test-data/t10k-labels-idx1-ubyte", "r");
    const buffer = Buffer.alloc(4);
    await labelsFile.read(buffer, 0, 4, position);
    position += 4;
    const magicNumber = buffer.readInt32BE();
    await labelsFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfItems = buffer.readInt32BE();
    const labels = [];
    for (let i = 0; i < numberOfItems; i++) {
      await labelsFile.read(buffer, 0, 1, position);
      position += 1;
      const label = buffer.readInt8();
      labels.push(label);
      console.log("\033[2J");
      console.log(`Reading image label ${i + 1} out of ${numberOfItems}`);
    }

    labelsFile.close();

    return labels;
  } catch (e) {
    console.log(e);
  }
};

const loadTestImagesData = async () => {
  try {
    let position = 0;

    const imagesFile = await fs.open("./test-data/t10k-images-idx3-ubyte", "r");
    const buffer = Buffer.alloc(4);
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const magicNumber = buffer.readInt32BE();
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfItems = buffer.readInt32BE();
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfRows = buffer.readInt32BE();
    await imagesFile.read(buffer, 0, 4, position);
    position += 4;
    const numberOfColumns = buffer.readInt32BE();
    const images = [];
    for (let i = 0; i < numberOfItems; i++) {
      const image = [];
      for (let j = 0; j < numberOfRows; j++) {
        for (let k = 0; k < numberOfColumns; k++) {
          await imagesFile.read(buffer, 0, 1, position);
          position += 1;
          const pixel = buffer.readInt8();
          image.push(pixel);
        }
      }
      console.log("\033[2J");
      console.log(`Reading image ${i + 1} out of ${numberOfItems}`);
      images.push(image);
    }

    imagesFile.close();

    return images;
  } catch (e) {
    console.log(e);
  }
};

const readTrainingData = async () => {
  const labels = await loadTrainingLabelsData();
  const images = await loadTrainingImagesData();

  const data = [];
  for (let i = 0; i < labels.length; i++) {
    data.push({
      image: images[i],
      label: labels[i]
    });
  }

  return data;
};

const readTestData = async () => {
  const labels = await loadTestLabelsData();
  const images = await loadTestImagesData();

  const data = [];
  for (let i = 0; i < labels.length; i++) {
    data.push({
      image: images[i],
      label: labels[i]
    });
  }

  return data;
};

//readTrainingData().then(data => console.log(data));

const getExpectedOutput = label => {
  const output = [];
  for (let i = 0; i < 10; i++) {
    if (label === i) {
      output.push(1);
    } else {
      output.push(0);
    }
  }

  return output;
};

function shuffle(array) {
  var currentIndex = array.length,
    temporaryValue,
    randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

const train = async () => {
  let data = await readTrainingData();
  const brain = new Brain(2, 16, data[0].image.length);
  //console.log("input", data[0].image.length);
  for (let i = 0; i < 2000; i++) {
    global.gc();
    data = shuffle(data);
    data.forEach(it => {
      brain.setInputActivations(it.image);
      console.log(it.label);
      brain.calculateOutput();
      const cost = brain.calculateCost(getExpectedOutput(it.label));
      console.log("cost:", cost);
      brain.train(getExpectedOutput(it.label), 100);
    });
  }

  /// test
  data = await readTestData();
  let avgCost = 0;
  data.forEach(it => {
    brain.setInputActivations(it.image);
    console.log(it.label);
    brain.calculateOutput();
    const cost = brain.calculateCost(getExpectedOutput(it.label));
    avgCost += cost;
    console.log("cost:", cost);
  });
  avgCost = avgCost / data.length;
  console.log("avg cost training set:", avgCost);
};

train();
