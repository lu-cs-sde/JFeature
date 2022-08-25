/* Copyright (c) 2021, Idriss Riouak <idriss.riouak@cs.lth.se>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from this
 * software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

package org.extendj;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.TreeSet;
import org.extendj.JavaChecker;
import org.extendj.ast.CompilationUnit;
import org.extendj.ast.Frontend;
import org.extendj.ast.Program;
import org.extendj.feature.Feature;

/**
 * Perform static semantic checks on a Java program.
 */
public class App extends Frontend {

  public static Object DrAST_root_node;
  private static String projectName;
  private static String filename;

  private String[] setEnv(String[] args) throws FileNotFoundException {
    if (args.length < 1) {
      System.err.println("You must specify a source file on the command line!");
    }

    ArrayList<String> FEOptions = new ArrayList<>();
    filename = args[0];
    for (int i = 0; i < args.length; ++i) {
      String opt = args[i];
      if (opt.contains(".java") || opt.contains(".tmp")) {
        FEOptions.add(args[i]);
        continue;
      }
      if (opt.startsWith("-prjname=")) {
        projectName = opt.substring(9, opt.length());
        continue;
      }

      switch (opt) {
      case "-nowarn":
        FEOptions.add("-nowarn");
        break;
      case "-classpath":
        FEOptions.add("-classpath");
        FEOptions.add(args[++i]);
        break;
      default:
        System.err.println("Unrecognized option: " + opt);
      }
    }

    return FEOptions.toArray(new String[FEOptions.size()]);
  }

  /**
   * Entry point for the Java checker.
   * @param args command-line arguments
   */
  public static void main(String args[])
      throws FileNotFoundException, InterruptedException, IOException {
    App app = new App();

    String[] jCheckerArgs = app.setEnv(args);
    int exitCode = app.run(jCheckerArgs);
    DrAST_root_node = app.getEntryPoint();
    printProgramInspection(app.getEntryPoint());
  }

  /**
   * Initialize the Java checker.
   */
  public App() { super("App", ExtendJVersion.getVersion()); }

  /**
   * @param args command-line arguments
   * @return {@code true} on success, {@code false} on error
   * @deprecated Use run instead!
   */
  @Deprecated
  public static boolean compile(String args[]) {
    return 0 == new JavaChecker().run(args);
  }

  /**
   * Run the Java checker.
   * @param args command-line arguments
   * @return 0 on success, 1 on error, 2 on configuration error, 3 on system
   */
  public int run(String args[]) {
    return run(args, Program.defaultBytecodeReader(),
               Program.defaultJavaParser());
  }

  @Override
  protected String name() {
    return "Feature";
  }

  @Override
  protected String version() {
    return "SCAM2022";
  }

  public Program getEntryPoint() { return program; }

  // Extracts all the Feature in the collection Program.features() and prints
  // all the fields accessible with a getter in a csv file named
  // filename_features.csv
  static void printProgramInspection(Program _program) {
    String filename = projectName + "features.csv";
    Utils.printInfo(System.out, "Printing features in " + filename);
    File file = new File(filename);
    try {
      file.createNewFile();
    } catch (IOException e) {
      e.printStackTrace();
    }
    try (FileWriter writer = new FileWriter(file)) {
      // writer.write("Version, Feature, Url\n");
      for (Feature f : _program.features()) {
        writer.write(f.getCluster() + "," + f.getFeatureID() + "," +
                     f.getUrl() + "," + projectName + "\n");
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
