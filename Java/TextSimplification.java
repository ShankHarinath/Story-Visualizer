import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.stream.Stream;

import org.apache.commons.lang3.tuple.Pair;

import com.google.common.collect.ImmutableMultimap;

import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefChain.CorefMention;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.logging.RedwoodConfiguration;

@SuppressWarnings("serial")
public class TextSimplification {

	public static List<String> replacementList = new ArrayList<String>() {{
		add("he");
		add("him");
		add("his");
		add("she");
		add("her");
		add("it");
		add("they");
		add("them");
		add("their");
		add("i");
		add("its");
		add("her's");
		add("that");
		add("you");
		add("your");
		add("your's");
		add("mine");
		add("my");
		add("this");
	}};

	public static String resolvedSentences = "";

	private final static String PCG_MODEL = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";        

	private final static TokenizerFactory<CoreLabel> tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "invertible=true");

	private static final LexicalizedParser parser = LexicalizedParser.loadModel(PCG_MODEL);

	public static void main(String[] args) throws IOException 
	{
		String text = new String(Files.readAllBytes(Paths.get(args[0])), StandardCharsets.UTF_8);
		text = text.replace("\n", " ");

		//Resolve Anaphora
		System.out.println("Anaphora Resolution...");
		resolveAnaphora(text);
		System.out.println("Anaphora Resolution Completed!\nIntermediate Output in \"AnaphoraResolved.txt\"");
		writeToFile(resolvedSentences, "AnaphoraResolved.txt");

		//Create ParseTrees
		System.out.println("Parse Tree Generation...");
		startParsing((resolvedSentences));
		System.out.println("Parse Tree Generation Completed!\nIntermediate Output in \"Tree.txt\"");
	}

	public static void resolveAnaphora(String text){

		RedwoodConfiguration.empty().capture(System.err).apply();

		Annotation document = new Annotation(text);
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
		props.put("dcoref.female", "female.unigram.txt");
		props.put("dcoref.male", "male.unigram.txt");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(document);
		
		RedwoodConfiguration.current().clear().apply();

		Map<Integer, CorefChain> graph = document.get(CorefChainAnnotation.class);
		List<CoreMap> stnfrdSentences = document.get(SentencesAnnotation.class);

		ImmutableMultimap.Builder<Integer, Pair<CorefChain, CorefMention>> records = ImmutableMultimap.builder();
		ImmutableMultimap.Builder<Integer, Pair<CorefChain, CorefMention>> recordsOrdered = ImmutableMultimap.builder();

		graph.forEach((key, value) -> {
			value.getMentionMap().forEach((intPair, corefSet) -> {
				corefSet.forEach(mention -> records.put(mention.sentNum, Pair.of(value, mention)));
			});
		});

		recordsOrdered = records.orderKeysBy(new Comparator<Integer>() {
			@Override
			public int compare(Integer o1, Integer o2) {
				return o1 - o2;
			}
		});

		recordsOrdered.build().asMap().forEach((sentNum, mentionList) -> {
			Stream<Pair<CorefChain, CorefMention>> list = mentionList.stream().sorted(new Comparator<Pair<CorefChain, CorefMention>>() {
				@Override
				public int compare(Pair<CorefChain, CorefMention> o1,
						Pair<CorefChain, CorefMention> o2) {
					return o1.getRight().startIndex - o2.getRight().startIndex;
				}
			});
			CoreMap sentence = stnfrdSentences.get(sentNum-1);
			List<CoreLabel> stnfrdtokens = sentence.get(TokensAnnotation.class);
			
			list.forEach(pair -> {
				CorefChain chain = pair.getLeft();
				CorefMention mention = pair.getRight();
				String root = chain.getRepresentativeMention().mentionSpan;

				if(!mention.mentionSpan.equalsIgnoreCase(root) 
						&& replacementList.contains(mention.mentionSpan.toLowerCase())){
					if(mention.mentionSpan.equalsIgnoreCase("her") || mention.mentionSpan.equalsIgnoreCase("his")){
						root += "'s";
					}
					stnfrdtokens.get(mention.startIndex-1).setOriginalText(root);
				}
			});

			String sent = "";
			for(CoreLabel token : stnfrdtokens){
				sent += token.originalText() + " ";
			};
			resolvedSentences += sent + "\n";
		});
	}

	public static Tree parse(String str) {                
		List<CoreLabel> tokens = tokenize(str);
		Tree tree = parser.apply(tokens);
		return tree;
	}

	private static List<CoreLabel> tokenize(String str) {
		Tokenizer<CoreLabel> tokenizer =
				tokenizerFactory.getTokenizer(new StringReader(str));    
		return tokenizer.tokenize();
	}

	public static void startParsing(String paragraph) throws FileNotFoundException, IOException 
	{ 
		String parseTrees = "";

		//Can we just split on new line as paragraph is already sentence splitted.
		Reader reader = new StringReader(paragraph);
		DocumentPreprocessor dp = new DocumentPreprocessor(reader);
		List<String> sentenceList = new ArrayList<String>();

		for (List<HasWord> sentence : dp) {
			String sentenceString = Sentence.listToString(sentence);
			sentenceList.add(sentenceString.toString());
		}

		for (String sentence : sentenceList) 
		{
			//			System.out.println(sentence);
			parseTrees += createParseTree(sentence);
		}
		writeToFile(parseTrees, "trees.txt");        
	}

	public static void writeToFile(String content, String filename) throws IOException
	{
		File file = new File(filename);
		file.delete();

		FileWriter fout = new FileWriter(filename);
		fout.write(content);
		fout.close();
	}

	public static String createParseTree(String sentence)
	{
		Tree tree = parse(sentence);  
		//		System.out.println(tree.toString());
		return (tree.toString()+"\n");
	}
}
