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
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;


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

	public static void main(String[] args) {

		String text = "Harriet Beecher is a writer."
				+ " She was born in Litchfield, Connecticut, USA, the daughter of Lyman Beecher."
				+ " Raised by her severe Calvinist father, she was educated and then taught at the Hartford "
				+ "Female Seminary (founded by her sister Catherine Beecher). "
				+ "Moving to Cincinnati with her father (in 1832), she began to write short fiction, and "
				+ "after her marriage (in 1836) persevered in her writing while raising seven children.";
		
		resolveAnaphora(text);
		System.out.println(resolvedSentences);
	}
	
	public static void resolveAnaphora(String text){
		
		Annotation document = new Annotation(text);
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
		props.put("dcoref.female", "/Users/Shank/Desktop/Stanford/females.txt");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(document);

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
}
