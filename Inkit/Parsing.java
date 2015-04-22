import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.trees.Tree;

class Parsing {

	private final static String PCG_MODEL = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";        

	private final TokenizerFactory<CoreLabel> tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "invertible=true");

	private final LexicalizedParser parser = LexicalizedParser.loadModel(PCG_MODEL);

	public Tree parse(String str) {                
		List<CoreLabel> tokens = tokenize(str);
		Tree tree = parser.apply(tokens);
		return tree;
	}

	private List<CoreLabel> tokenize(String str) {
		Tokenizer<CoreLabel> tokenizer =
		tokenizerFactory.getTokenizer(new StringReader(str));    
		return tokenizer.tokenize();
	}

	public static void main(String[] args) throws FileNotFoundException, IOException 
	{ 
		String parseTrees = "";
		String paragraph = new String(Files.readAllBytes(Paths.get("input.txt")), StandardCharsets.UTF_8);
		paragraph = paragraph.replace("\n", " ");

		Reader reader = new StringReader(paragraph);
		DocumentPreprocessor dp = new DocumentPreprocessor(reader);
		List<String> sentenceList = new ArrayList<String>();

		for (List<HasWord> sentence : dp) {
			String sentenceString = Sentence.listToString(sentence);
			sentenceList.add(sentenceString.toString());
		}

		for (String sentence : sentenceList) 
		{
			System.out.println(sentence);
			parseTrees += createParseTree(sentence);
		}
		writeParseTreeToFile(parseTrees);        


	}
	public static void writeParseTreeToFile(String parseTrees) throws IOException
	{
		FileWriter fout = new FileWriter("trees.txt");
		String[] trees = parseTrees.split("\\r?\\n");
		for(String tree : trees)
		{
			fout.write(tree);
			fout.write("\n");
		}
		fout.close();
	}
	public static String createParseTree(String sentence)
	{
		Parsing parser = new Parsing(); 
		Tree tree = parser.parse(sentence);  
		System.out.println(tree.toString());
		return (tree.toString()+"\n");
	}
}