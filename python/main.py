# http://yann.lecun.com/exdb/mnist/
from network import Brain
from random import shuffle
import pickle
MAX_TRAINING_SIZE = 60000

# const fs = require("fs").promises;
# const Brain = require("./Brain");


def load_training_labels_data(addr, ammount):
    with open(
        addr,
        "rb"
    ) as f:
        _magic_number = int.from_bytes(f.read(4), byteorder="big")
        number_of_items = int.from_bytes(f.read(4), byteorder="big")
        labels = []
        for i in range(min(number_of_items, ammount)):
            label = ord(f.read(1))
            labels.append(label)
            print("\033[2J")
            print("Reading image label " + str((i + 1)) +
                  " out of " + str(number_of_items))
        return labels


def load_training_images_data(addr, ammount):
    with open(
        addr,
        "rb"
    ) as f:
        _magic_number = int.from_bytes(f.read(4), byteorder="big")
        number_of_items = int.from_bytes(f.read(4), byteorder="big")
        number_of_rows = int.from_bytes(f.read(4), byteorder="big")
        number_of_columns = int.from_bytes(f.read(4), byteorder="big")
        images = []
        for i in range(min(number_of_items, ammount)):
            image = []
            for _ in range(number_of_rows):
                for _ in range(number_of_columns):
                    pixel = ord(f.read(1))
                    image.append(pixel/255)
            images.append(image)
            print("\033[2J")
            print("Reading image " + str((i + 1)) +
                  " out of " + str(number_of_items))
        return images

# const loadTrainingImagesData = async () => {
#   try {
#     let position = 0;

#     const imagesFile = await fs.open(
#       "./training-data/train-images-idx3-ubyte",
#       "r"
#     );
#     const buffer = Buffer.alloc(4);
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const magicNumber = buffer.readInt32BE();
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfItems = buffer.readInt32BE();
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfRows = buffer.readInt32BE();
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfColumns = buffer.readInt32BE();
#     const images = [];
#     for (let i = 0; i < numberOfItems && i < MAX_TRAINING_SIZE; i++) {
#       const image = [];
#       for (let j = 0; j < numberOfRows; j++) {
#         for (let k = 0; k < numberOfColumns; k++) {
#           await imagesFile.read(buffer, 0, 1, position);
#           position += 1;
#           const pixel = buffer.readInt8();
#           image.push(pixel);
#         }
#       }
#       console.log("\033[2J");
#       console.log(`Reading image ${i + 1} out of ${numberOfItems}`);
#       images.push(image);
#     }

#     imagesFile.close();

#     return images;
#   } catch (e) {
#     console.log(e);
#   }
# };

# const loadTestLabelsData = async () => {
#   try {
#     let position = 0;

#     const labelsFile = await fs.open("./test-data/t10k-labels-idx1-ubyte", "r");
#     const buffer = Buffer.alloc(4);
#     await labelsFile.read(buffer, 0, 4, position);
#     position += 4;
#     const magicNumber = buffer.readInt32BE();
#     await labelsFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfItems = buffer.readInt32BE();
#     const labels = [];
#     for (let i = 0; i < numberOfItems; i++) {
#       await labelsFile.read(buffer, 0, 1, position);
#       position += 1;
#       const label = buffer.readInt8();
#       labels.push(label);
#       console.log("\033[2J");
#       console.log(`Reading image label ${i + 1} out of ${numberOfItems}`);
#     }

#     labelsFile.close();

#     return labels;
#   } catch (e) {
#     console.log(e);
#   }
# };

# const loadTestImagesData = async () => {
#   try {
#     let position = 0;

#     const imagesFile = await fs.open("./test-data/t10k-images-idx3-ubyte", "r");
#     const buffer = Buffer.alloc(4);
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const magicNumber = buffer.readInt32BE();
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfItems = buffer.readInt32BE();
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfRows = buffer.readInt32BE();
#     await imagesFile.read(buffer, 0, 4, position);
#     position += 4;
#     const numberOfColumns = buffer.readInt32BE();
#     const images = [];
#     for (let i = 0; i < numberOfItems; i++) {
#       const image = [];
#       for (let j = 0; j < numberOfRows; j++) {
#         for (let k = 0; k < numberOfColumns; k++) {
#           await imagesFile.read(buffer, 0, 1, position);
#           position += 1;
#           const pixel = buffer.readInt8();
#           image.push(pixel);
#         }
#       }
#       console.log("\033[2J");
#       console.log(`Reading image ${i + 1} out of ${numberOfItems}`);
#       images.push(image);
#     }

#     imagesFile.close();

#     return images;
#   } catch (e) {
#     console.log(e);
#   }
# };


def read_training_data():
    labels = load_training_labels_data(
        "./training-data/train-labels-idx1-ubyte", MAX_TRAINING_SIZE)
    images = load_training_images_data(
        "./training-data/train-images-idx3-ubyte", MAX_TRAINING_SIZE)
    return list(zip(labels, images))


def read_testing_data():
    labels = load_training_labels_data(
        "./test-data/t10k-labels-idx1-ubyte", 10000)
    images = load_training_images_data(
        "./test-data/t10k-images-idx3-ubyte", 10000)
    return list(zip(labels, images))

# const readTestData = async () => {
#   const labels = await loadTestLabelsData();
#   const images = await loadTestImagesData();

#   const data = [];
#   for (let i = 0; i < labels.length; i++) {
#     data.push({
#       image: images[i],
#       label: labels[i]
#     });
#   }

#   return data;
# };

# //readTrainingData().then(data => console.log(data));


def get_expected_output(label):
    output = []
    for i in range(10):
        if label == i:
            output.append(1)
        else:
            output.append(0)
    return output


def save_net_status(net, file):
    with open(file, 'wb') as output:
        pickle.dump(net, output, pickle.HIGHEST_PROTOCOL)


def load_net(file):
    with open(file, 'rb') as input:
        return pickle.load(input)


def train():
    data = read_training_data()
    # brain = Brain(2, 32, len(data[0][1]))
    brain = load_net("network_save")
    for _i in range(1):
        shuffle(data)
        cost = 0
        for d in data:
            brain.set_input_activations(d[1])
            # print(str(d[0]))
            brain.calculate_output()
            cost += brain.calculate_cost(get_expected_output(d[0]))
            #print("cost: " + str(cost))
            brain.train(get_expected_output(d[0]), 2)
        print(cost/(len(data)))
        cost = 0
        print("saving net")
        save_net_status(brain, "network_save")


def test():
    brain = load_net("network_save")
    data = read_testing_data()
    cost = 0
    for d in data:
        brain.set_input_activations(d[1])
        brain.calculate_output()
        cost += brain.calculate_cost(get_expected_output(d[0]))

    print("final cost", cost/(len(data)))


train()
test()

#   /// test
#   data = await readTestData();
#   let avgCost = 0;
#   data.forEach(it => {
#     brain.setInputActivations(it.image);
#     console.log(it.label);
#     brain.calculateOutput();
#     const cost = brain.calculateCost(getExpectedOutput(it.label));
#     avgCost += cost;
#     console.log("cost:", cost);
#   });
#   avgCost = avgCost / data.length;
#   console.log("avg cost training set:", avgCost);
# };

# train();
