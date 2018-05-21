package edu.kaist.mrlab.nn.pcnn.prepro;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Iterator;

import edu.kaist.mrlab.nn.pcnn.utilities.GlobalVariables;
import edu.kaist.mrlab.nn.pcnn.utilities.OntoProperty;

/**
 * 
 * @author sangha
 *
 */
public class TrainTestSetSeperator {

	public void divide(String property) {

		try {
			
			File f = new File("data/ds/train_test_" + GlobalVariables.option + "/");
			if(!f.exists()) {
				f.mkdirs();
			}

			Path inputPath = Paths.get("data/ds/total_" + GlobalVariables.option + "/" + property);
			Path trainOutPath = Paths
					.get("data/ds/train_test_" + GlobalVariables.option + "/" + property + "_train");
			Path testOutPath = Paths
					.get("data/ds/train_test_" + GlobalVariables.option + "/" + property + "_test");

			BufferedReader br = Files.newBufferedReader(inputPath);
			BufferedWriter bwTrain = Files.newBufferedWriter(trainOutPath);
			BufferedWriter bwTest = Files.newBufferedWriter(testOutPath);

			int totalCount = (int) br.lines().count();
			int testCount = (int) (totalCount * GlobalVariables.testRatio);
//			int testCount = 1;
			

			br.close();

			br = Files.newBufferedReader(inputPath);
			Iterator<String> brit = br.lines().iterator();

			int count = 0;
			while (brit.hasNext()) {

				if (count < testCount) {
					bwTest.write(brit.next() + "\n");
				} else {
					bwTrain.write(brit.next() + "\n");
				}

				count++;
			}

			bwTrain.close();
			bwTest.close();
			br.close();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] ar) {

		System.out.println("Divide total to train and test");

		TrainTestSetSeperator ttss = new TrainTestSetSeperator();
		for (OntoProperty p : OntoProperty.values()) {

			String property = p.toString();
			if (property.equals("classP")) {
				property = "class";
			}

			System.out.print(property + "...");

			ttss.divide(property);

			System.out.println("Done!");

		}
	}

}
