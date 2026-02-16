import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => ReaderModel(),
      child: const SpeedReaderApp(),
    ),
  );
}

class SpeedReaderApp extends StatelessWidget {
  const SpeedReaderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ZapRead',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: Colors.black,
        colorScheme: const ColorScheme.dark(
          primary: Colors.red,
          surface: Colors.black,
        ),
      ),
      home: const HomeScreen(),
    );
  }
}

/// Calculate ORP index for a word — closer to center for longer words
int orpIndex(String word) {
  final len = word.length;
  if (len <= 1) return 0;
  if (len <= 3) return 1; // middle-ish
  // For 4+ chars, pick ~40% position (balances readability & centering)
  return ((len - 1) * 0.4).round().clamp(1, len - 2);
}

class ReaderModel extends ChangeNotifier {
  List<String> _words = [];
  int _currentIndex = 0;
  int _wpm = 300;
  bool _isPlaying = false;
  Timer? _timer;
  String _inputText = '';

  List<String> get words => _words;
  int get currentIndex => _currentIndex;
  int get wpm => _wpm;
  bool get isPlaying => _isPlaying;
  String get inputText => _inputText;
  String get currentWord => _words.isNotEmpty && _currentIndex < _words.length
      ? _words[_currentIndex]
      : '';
  double get progress =>
      _words.isEmpty ? 0 : _currentIndex / (_words.length - 1).clamp(1, double.infinity);

  void setText(String text) {
    _inputText = text;
    _words = text.split(RegExp(r'\s+')).where((w) => w.isNotEmpty).toList();
    _currentIndex = 0;
    _isPlaying = false;
    _timer?.cancel();
    notifyListeners();
  }

  void setWpm(int value) {
    _wpm = value;
    if (_isPlaying) {
      _startTimer();
    }
    notifyListeners();
  }

  void togglePlay() {
    if (_words.isEmpty) return;
    _isPlaying = !_isPlaying;
    if (_isPlaying) {
      if (_currentIndex >= _words.length - 1) {
        _currentIndex = 0;
      }
      _startTimer();
    } else {
      _timer?.cancel();
    }
    notifyListeners();
  }

  void startPlaying() {
    if (_words.isEmpty) return;
    if (_isPlaying) return;
    if (_currentIndex >= _words.length - 1) {
      _currentIndex = 0;
    }
    _isPlaying = true;
    _startTimer();
    notifyListeners();
  }

  void stopPlaying() {
    if (!_isPlaying) return;
    _isPlaying = false;
    _timer?.cancel();
    notifyListeners();
  }

  void reset() {
    _currentIndex = 0;
    _isPlaying = false;
    _timer?.cancel();
    notifyListeners();
  }

  /// Jump back ~10 seconds worth of words at current WPM
  void jumpBack() {
    final wordsBack = (_wpm * 10 / 60).round().clamp(1, _words.length);
    _currentIndex = (_currentIndex - wordsBack).clamp(0, _words.length - 1);
    if (_isPlaying) _startTimer(); // restart timer from new position
    notifyListeners();
  }

  void _startTimer() {
    _timer?.cancel();
    final interval = Duration(milliseconds: (60000 / _wpm).round());
    _timer = Timer.periodic(interval, (_) {
      if (_currentIndex < _words.length - 1) {
        _currentIndex++;
        notifyListeners();
      } else {
        _isPlaying = false;
        _timer?.cancel();
        notifyListeners();
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}

const String sampleText =
    'Speed reading is a collection of methods that aim to increase rates of reading '
    'without greatly reducing comprehension or retention. These methods include chunking '
    'and minimizing subvocalization. The many available speed reading training programs '
    'include books, videos, software, and seminars. The underlying claim behind speed '
    'reading is that the normal method of reading is actually inefficient. By using '
    'techniques like rapid serial visual presentation you can train your brain to process '
    'words much faster than the average reading speed of around 250 words per minute. '
    'Some practitioners claim to read at speeds of over 1000 words per minute while '
    'maintaining good comprehension. Whether these claims hold up under scientific '
    'scrutiny is debatable but the techniques are certainly interesting to explore.';

class HomeScreen extends HookWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final model = context.watch<ReaderModel>();
    final hasText = model.words.isNotEmpty;

    if (!hasText) {
      return const TextInputScreen();
    }
    return const ReaderScreen();
  }
}

class TextInputScreen extends HookWidget {
  const TextInputScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final controller = useTextEditingController();
    final model = context.read<ReaderModel>();

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 40),
              const Text(
                'BLITZREAD',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  letterSpacing: 4,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Speed read with ORP highlighting',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.white38,
                  letterSpacing: 2,
                ),
              ),
              const SizedBox(height: 40),
              Expanded(
                child: TextField(
                  controller: controller,
                  maxLines: null,
                  expands: true,
                  textAlignVertical: TextAlignVertical.top,
                  style: const TextStyle(color: Colors.white70, fontSize: 16),
                  decoration: InputDecoration(
                    hintText: 'Paste or type your text here...',
                    hintStyle: const TextStyle(color: Colors.white24),
                    filled: true,
                    fillColor: Colors.white.withValues(alpha: 0.05),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: Colors.red, width: 1),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () {
                        if (controller.text.trim().isNotEmpty) {
                          model.setText(controller.text.trim());
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text(
                        'START READING',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 2,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              TextButton(
                onPressed: () {
                  controller.text = sampleText;
                },
                child: const Text(
                  'Load sample text',
                  style: TextStyle(color: Colors.white38),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ReaderScreen extends HookWidget {
  const ReaderScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final model = context.watch<ReaderModel>();
    final word = model.currentWord;
    final orp = orpIndex(word);

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // Progress bar
            LinearProgressIndicator(
              value: model.progress,
              backgroundColor: Colors.white10,
              valueColor: const AlwaysStoppedAnimation<Color>(Colors.red),
              minHeight: 3,
            ),
            // Back button & word count
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back, color: Colors.white38),
                    onPressed: () {
                      model.stopPlaying();
                      model.reset();
                      model.setText('');
                    },
                  ),
                  Text(
                    '${model.currentIndex + 1} / ${model.words.length}',
                    style: const TextStyle(color: Colors.white38, fontSize: 14),
                  ),
                ],
              ),
            ),
            // Word display - tap to toggle play/pause
            Expanded(
              child: GestureDetector(
                onTap: () => model.togglePlay(),
                behavior: HitTestBehavior.opaque,
                child: Center(
                  child: word.isEmpty
                      ? const Text(
                          'Tap to start reading',
                          style: TextStyle(color: Colors.white24, fontSize: 20),
                        )
                      : AnimatedSwitcher(
                          duration: const Duration(milliseconds: 200),
                          child: model.isPlaying
                              ? KeyedSubtree(
                                  key: const ValueKey('orp'),
                                  child: _buildOrpWord(word, orp),
                                )
                              : KeyedSubtree(
                                  key: const ValueKey('context'),
                                  child: _buildContextView(model),
                                ),
                        ),
                ),
              ),
            ),
            // Controls
            Container(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  // Play/Pause + Reset
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        iconSize: 32,
                        icon: const Icon(Icons.replay_10, color: Colors.white38),
                        onPressed: () => model.jumpBack(),
                      ),
                      const SizedBox(width: 24),
                      GestureDetector(
                        onTap: () => model.togglePlay(),
                        child: Container(
                          width: 64,
                          height: 64,
                          decoration: BoxDecoration(
                            color: model.isPlaying ? Colors.red.shade700 : Colors.red,
                            shape: BoxShape.circle,
                          ),
                          child: Icon(
                            model.isPlaying ? Icons.pause : Icons.play_arrow,
                            color: Colors.white,
                            size: 40,
                          ),
                        ),
                      ),
                      const SizedBox(width: 24),
                      const SizedBox(width: 32), // spacer for symmetry
                    ],
                  ),
                  const SizedBox(height: 24),
                  // WPM slider
                  Row(
                    children: [
                      const Text(
                        'WPM',
                        style: TextStyle(color: Colors.white38, fontSize: 12),
                      ),
                      Expanded(
                        child: Slider(
                          value: model.wpm.toDouble(),
                          min: 100,
                          max: 1000,
                          divisions: 18,
                          activeColor: Colors.red,
                          inactiveColor: Colors.white12,
                          onChanged: (v) => model.setWpm(v.round()),
                        ),
                      ),
                      SizedBox(
                        width: 48,
                        child: Text(
                          '${model.wpm}',
                          textAlign: TextAlign.right,
                          style: const TextStyle(
                            color: Colors.white70,
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Build the paused context view — paragraph with current word highlighted
  Widget _buildContextView(ReaderModel model) {
    final words = model.words;
    final idx = model.currentIndex;
    // Show ~80 words around current word
    final start = (idx - 40).clamp(0, words.length);
    final end = (idx + 41).clamp(0, words.length);

    // Build spans with fading opacity based on distance from current word
    List<InlineSpan> spans = [];
    for (int i = start; i < end; i++) {
      final distance = (i - idx).abs();
      final opacity = (1.0 - distance * 0.03).clamp(0.1, 1.0);

      if (i == idx) {
        // Current word with ORP highlight
        final w = words[i];
        final orp = orpIndex(w);
        final before = w.substring(0, orp);
        final letter = w[orp];
        final after = w.substring(orp + 1);
        if (before.isNotEmpty) {
          spans.add(TextSpan(
            text: before,
            style: TextStyle(
              color: Colors.white.withValues(alpha: opacity),
              fontSize: 22,
              fontWeight: FontWeight.bold,
              height: 1.6,
            ),
          ));
        }
        spans.add(TextSpan(
          text: letter,
          style: TextStyle(
            color: Colors.red.withValues(alpha: opacity),
            fontSize: 22,
            fontWeight: FontWeight.bold,
            height: 1.6,
          ),
        ));
        if (after.isNotEmpty) {
          spans.add(TextSpan(
            text: after,
            style: TextStyle(
              color: Colors.white.withValues(alpha: opacity),
              fontSize: 22,
              fontWeight: FontWeight.bold,
              height: 1.6,
            ),
          ));
        }
      } else {
        spans.add(TextSpan(
          text: words[i],
          style: TextStyle(
            color: Colors.white.withValues(alpha: opacity * 0.6),
            fontSize: 20,
            fontWeight: FontWeight.w300,
            height: 1.6,
          ),
        ));
      }
      if (i < end - 1) {
        final spaceOpacity = ((1.0 - distance * 0.08) * 0.6).clamp(0.1, 0.6);
        spans.add(TextSpan(
          text: ' ',
          style: TextStyle(
            color: Colors.white.withValues(alpha: spaceOpacity),
            fontSize: 20,
            height: 1.6,
          ),
        ));
      }
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 32),
      child: ShaderMask(
        shaderCallback: (bounds) => LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            Colors.transparent,
            Colors.white,
            Colors.white,
            Colors.transparent,
          ],
          stops: const [0.0, 0.15, 0.85, 1.0],
        ).createShader(bounds),
        blendMode: BlendMode.dstIn,
        child: RichText(
          textAlign: TextAlign.center,
          text: TextSpan(children: spans),
        ),
      ),
    );
  }

  /// Build the word with ORP letter highlighted and aligned to center
  Widget _buildOrpWord(String word, int orp) {
    final before = word.substring(0, orp);
    final letter = word[orp];
    final after = word.substring(orp + 1);

    const style = TextStyle(
      fontSize: 48,
      fontWeight: FontWeight.w300,
      fontFamily: 'monospace',
      color: Colors.white,
      height: 1,
    );
    const redStyle = TextStyle(
      fontSize: 48,
      fontWeight: FontWeight.bold,
      fontFamily: 'monospace',
      color: Colors.red,
      height: 1,
    );

    // Measure widths
    final beforePainter = TextPainter(
      text: TextSpan(text: before, style: style),
      textDirection: TextDirection.ltr,
    )..layout();

    final letterPainter = TextPainter(
      text: TextSpan(text: letter, style: redStyle),
      textDirection: TextDirection.ltr,
    )..layout();

    final afterPainter = TextPainter(
      text: TextSpan(text: after, style: style),
      textDirection: TextDirection.ltr,
    )..layout();

    // Distance from left edge of word to center of ORP letter
    final orpOffset = beforePainter.width + letterPainter.width / 2;
    final totalWidth = beforePainter.width + letterPainter.width + afterPainter.width;
    // Distance from center of ORP to right edge
    final rightOfOrp = totalWidth - orpOffset;

    // Make both sides equal by padding the shorter side
    final maxSide = orpOffset > rightOfOrp ? orpOffset : rightOfOrp;
    final leftPad = maxSide - orpOffset;
    final rightPad = maxSide - rightOfOrp;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(width: leftPad),
        RichText(
          text: TextSpan(
            children: [
              if (before.isNotEmpty) TextSpan(text: before, style: style),
              TextSpan(text: letter, style: redStyle),
              if (after.isNotEmpty) TextSpan(text: after, style: style),
            ],
          ),
        ),
        SizedBox(width: rightPad),
      ],
    );
  }
}
