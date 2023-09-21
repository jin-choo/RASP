package main;

import algorithms.RASP.RASP;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

public class Main_saveToFile {

	public static void main(String[] arg) throws IOException {
		ArrayList<int[]> NIDsMotifNeuronsNumbersList = new ArrayList<>() {{
			add(new int[]{50, 5, 5});
		}};
//		add(new int[]{50, 5, 5});
//		add(new int[]{100, 5, 5}); add(new int[]{1000, 5, 5});
//		add(new int[]{50, 6, 5}); add(new int[]{50, 7, 5});
//		add(new int[]{200, 5, 5}); add(new int[]{300, 5, 5}); add(new int[]{500, 5, 5});
//		add(new int[]{50, 4, 5}); add(new int[]{50, 6, 5});
		ArrayList<Integer> recordingTimeList = new ArrayList<>() {{
			add(10);
			add(50);
			add(100);
			add(500);
			add(1000);
		}};
		ArrayList<Integer> binSizeList = new ArrayList<>() {{
			add(15);
			add(25);
			add(40);
		}};
		ArrayList<double[]> bgMtPpTjTwRangeBinsList = new ArrayList<>() {{
			add(new double[]{2.0, 0.2, 1.0, 0.0, 0.0, 1.0});
			add(new double[]{2.0, 0.2, 1.0, 10.0, 0.0, 1.0});
			add(new double[]{2.0, 0.2, 1.0, 20.0, 0.0, 1.0});
			add(new double[]{2.0, 0.2, 1.0, 10.0, 0.0, 2.0});
			add(new double[]{2.0, 0.2, 1.0, 20.0, 0.0, 2.0});
			add(new double[]{2.0, 0.2, 1.0, 10.0, 0.0, 3.0});
			add(new double[]{2.0, 0.2, 1.0, 20.0, 0.0, 3.0});
			add(new double[]{2.0, 0.4, 5.0, 10.0, 0.0, 1.0});
			add(new double[]{2.0, 0.4, 5.0, 10.0, 0.0, 2.0});
			add(new double[]{2.0, 0.4, 5.0, 10.0, 0.0, 3.0});
			add(new double[]{2.0, 0.2, 3.0, 30.0, 0.0, 1.0});
			add(new double[]{2.0, 0.2, 3.0, 30.0, 0.0, 2.0});
			add(new double[]{2.0, 0.2, 3.0, 30.0, 0.0, 3.0});
		}};

		ArrayList<int[]> motifTypeMaxList = new ArrayList<>() {{
			add(new int[]{2, 100, 0});
		}};
		ArrayList<Integer> seedList = new ArrayList<>() {{
			add(0);
			add(1);
			add(2);
		}};

		long timestamp = System.currentTimeMillis();
		Files.createDirectories(Paths.get("./txt"));
		for (int[] motifTypeMax : motifTypeMaxList) {
			BufferedWriter writerTime = new BufferedWriter(new FileWriter(String.format("./txt/%d_tree_tid_time_%s.csv", motifTypeMax[0], new SimpleDateFormat("MM.dd_HH.mm").format(timestamp))));
			writerTime.write("type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,inter,rangeBin,sup,k,#freq,time,seed");
			writerTime.newLine();
			writerTime.close();
		}

		ArrayList<ArrayList> totalList = new ArrayList<>() {{
			add(NIDsMotifNeuronsNumbersList);
			add(recordingTimeList);
			add(binSizeList);
			add(bgMtPpTjTwRangeBinsList);
			add(motifTypeMaxList);
			add(seedList);
		}};
		ArrayList<ArrayList> productList = cartesianProduct(0, totalList);
		productList.stream().forEach(resultList -> {
			int[] NIDsMotifNeuronsNumbers = (int[]) resultList.get(5);
			Integer recordingTime = (Integer) resultList.get(4);
			Integer binSize = (Integer) resultList.get(3);
			int NIDs = NIDsMotifNeuronsNumbers[0];
			double[] bgMtPpTjTwRangeBins = (double[]) resultList.get(2);
			double backgroundFiringRate = bgMtPpTjTwRangeBins[0];
			double motifFiringRate = bgMtPpTjTwRangeBins[1];
			double pp = bgMtPpTjTwRangeBins[2];
			int temporalJitter = (int) bgMtPpTjTwRangeBins[3];
			int timeWarping = (int) bgMtPpTjTwRangeBins[4];
			int rangeBins = (int) bgMtPpTjTwRangeBins[5];
			int motifNeurons = NIDsMotifNeuronsNumbers[1];
			int motifNumbers = NIDsMotifNeuronsNumbers[2];
			int[] motifTypeMax = (int[]) resultList.get(1);
			int motifType = motifTypeMax[0];
			int motifMaxLags = motifTypeMax[1];
			int motifMaxSpikes = motifTypeMax[2];
			int seed = (Integer) resultList.get(0);

			int winLen = (int) Math.ceil(100.0 / binSize);
			if (motifType > 1) {
				winLen = (int) Math.ceil((double) (motifNeurons - 1) * motifMaxLags / binSize);
			}

			try {
				RASP algo = new RASP();
				algo.runAlgorithm(motifType, NIDs, recordingTime, backgroundFiringRate, pp, temporalJitter, timeWarping, motifFiringRate, motifNeurons, motifNumbers, motifMaxLags, motifMaxSpikes, binSize, winLen, rangeBins, timestamp, seed);
				algo.printStats();
			} catch (OutOfMemoryError oome) {
				System.out.println(String.format("%s_NIDs_%d_time_%d_bg_%.2f_pp_%.1f_tj_%d_tw_%d_mt_%.2f_%d_%d_%d_%d_bin_%d_winlen_%d_inter_%d_seed_%d", motifType, NIDs, recordingTime, backgroundFiringRate, pp, temporalJitter, timeWarping, motifFiringRate, motifNeurons, motifNumbers, motifMaxLags, motifMaxSpikes, binSize, winLen, rangeBins, seed));
				System.err.println("Max JVM memory: " + Runtime.getRuntime().maxMemory());
			} catch (Exception e) {
				System.out.println(String.format("%s_NIDs_%d_time_%d_bg_%.2f_pp_%.1f_tj_%d_tw_%d_mt_%.2f_%d_%d_%d_%d_bin_%d_winlen_%d_inter_%d_seed_%d", motifType, NIDs, recordingTime, backgroundFiringRate, pp, temporalJitter, timeWarping, motifFiringRate, motifNeurons, motifNumbers, motifMaxLags, motifMaxSpikes, binSize, winLen, rangeBins, seed));
				e.printStackTrace();
			}
		});
	}

	public static ArrayList<ArrayList> cartesianProduct(int index, ArrayList<ArrayList> lists) {
		ArrayList<ArrayList> ret = new ArrayList<>();
		if (index == lists.size()) {
			ret.add(new ArrayList());
		} else {
			for (Object obj : lists.get(index)) {
				for (ArrayList set : cartesianProduct(index + 1, lists)) {
					set.add(obj);
					ret.add(set);
				}
			}
		}
		return ret;
	}
}